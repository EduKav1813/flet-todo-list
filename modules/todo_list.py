import flet as ft

from modules.db import Database, Session, TasksTable
from modules.task import Task


class TodoList(ft.UserControl):
    def build(self):
        self.items_left = ft.Text()
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()
        self.database = Database()
        self.load_tasks_from_database()
        self.update_active_items_left(
            len([task for task in self.tasks.controls if not task.model.completed])
        )

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.bind_tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        self.view = ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value="Todos", style="headlineMedium")],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Clear completed", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
        return self.view

    def update_database(self) -> None:
        """A method that saves the current state of the TodoList (Tasks) into the database."""
        with Session(self.database.engine) as session:
            if session.query(TasksTable).count() > 0:
                session.query(TasksTable).delete()

            for task in self.tasks.controls:
                new_task = TasksTable(
                    name=task.model.name,
                    description=task.model.description,
                    completed=task.model.completed,
                )
                session.add(new_task)

            session.commit()

    def load_tasks_from_database(self) -> None:
        """A method to set the current state of the TodoList (Tasks) from the database."""
        with Session(self.database.engine) as session:
            if session.query(TasksTable).count() > 0:
                tasks = session.query(TasksTable).all()
                for task in tasks:
                    new_task = Task(
                        task_name=task.name,
                        description=task.description,
                        completed=task.completed,
                        bind_task_status_change=self.bind_task_status_changed,
                        bind_task_delete=self.bind_task_delete,
                        bind_description_updated=self.bind_description_updated,
                    )
                    self.tasks.controls.append(new_task)

    def update_active_items_left(self, tasks_left: int):
        """Method to update the 'active items left' label.

        Args:
            tasks_left (int): The current amount of tasks left.
        """
        self.items_left.value = f"{tasks_left} active item(s) left"

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.model.completed)
                or (status == "completed" and task.model.completed)
            )

        tasks_left_count = [task.model.completed for task in self.tasks.controls].count(
            False
        )
        self.update_active_items_left(tasks_left_count)
        self.update_database()

        super().update()

    def bind_task_delete(self, task: Task) -> None:
        """Remove the given task from the TodoList

        Args:
            task (Task): Task to delete.
        """
        self.tasks.controls.remove(task)
        self.update()

    def bind_task_status_changed(self) -> None:
        """This method handles the event when the status of the Task in the TodoList was changed."""
        self.update()

    def add_clicked(self, e) -> None:
        """This method handles adding the new task in the TodoList, when user clicks the 'Add' button.

        If the Task name is empty, task will not be created.

        Args:
            e (_type_): _description_
        """
        label = self.new_task.value
        if label == "":
            return
        task = Task(
            task_name=label,
            description="Details",
            completed=False,
            bind_task_status_change=self.bind_task_status_changed,
            bind_task_delete=self.bind_task_delete,
            bind_description_updated=self.bind_description_updated,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def bind_tabs_changed(self, e) -> None:
        """This method handles the event of the user changing the current selected tab on the TodoList.

        Args:
            e (_type_): _description_
        """
        self.update()

    def clear_clicked(self, e) -> None:
        """This method handles the even of the clicking the 'Clear' button.
        This button clears all tasks that are in the 'completed' state.
        Tasks that are 'active' will remain on the list.

        Args:
            e (_type_): _description_
        """
        completed_tasks = [task for task in self.tasks.controls if task.model.completed]
        for task in completed_tasks:
            self.bind_task_delete(task)
        self.update()

    def bind_description_updated(self) -> None:
        """This method handles the event of the user modifying the description of the Task on the List."""
        self.update()
