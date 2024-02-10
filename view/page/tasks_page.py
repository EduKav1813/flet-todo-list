import flet as ft

from data.repositories.tasks_repository import TasksRepository, TaskStatusEnum
from entity.task import Task
from view.component.task_component import TaskComponent


class TasksPage(ft.UserControl):
    def build(self):
        self.items_left = ft.Text()
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()
        self.tasks_repository = TasksRepository()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.bind_tabs_changed,
            tabs=[
                ft.Tab(text=TaskStatusEnum.all.value),
                ft.Tab(text=TaskStatusEnum.active.value),
                ft.Tab(text=TaskStatusEnum.completed.value),
            ],
        )

        self.status = TaskStatusEnum.all
        self.load_tasks_from_database()

        self.update_active_items_left(
            len([task for task in self.tasks.controls if not task.model.completed])
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
        self.tasks_repository.update_all([task.model for task in self.tasks.controls])

    def load_tasks_from_database(self) -> None:
        """A method to set the current state of the TodoList (Tasks) from the database."""
        tasks = self.tasks_repository.get_all_by_status(self.status)
        self.tasks.controls = []
        for task in tasks:
            new_task = TaskComponent(
                model=task,
                on_task_status_changed=self.on_task_status_changed,
                on_task_deleted=self.on_task_deleted,
                on_name_updated=self.on_name_updated,
                on_description_updated=self.on_description_updated,
            )
            self.tasks.controls.append(new_task)

    def update_active_items_left(self, tasks_left: int):
        """Method to update the 'active items left' label.

        Args:
            tasks_left (int): The current amount of tasks left.
        """
        self.items_left.value = f"{tasks_left} active item(s) left"

    def update(self):
        tasks_left_count = [task.model.completed for task in self.tasks.controls].count(
            False
        )
        self.update_active_items_left(tasks_left_count)
        super().update()

    def on_task_deleted(self, task: TaskComponent) -> None:
        """Remove the given task from the TodoList

        Args:
            task (Task): Task to delete.
        """
        self.tasks.controls.remove(task)
        self.update()

    def on_task_status_changed(self) -> None:
        """This method handles the event when the status of the Task in the TodoList was changed."""
        self.tasks_repository.update_all([task.model for task in self.tasks.controls])
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
        task_entity = Task(name=label, description="Details", completed=False)
        self.tasks_repository.insert(task_entity)
        task_component = TaskComponent(
            model=task_entity,
            on_task_status_changed=self.on_task_status_changed,
            on_task_deleted=self.on_task_deleted,
            on_name_updated=self.on_name_updated,
            on_description_updated=self.on_description_updated,
        )
        self.tasks.controls.append(task_component)
        self.new_task.value = ""
        self.update()

    def bind_tabs_changed(self, e) -> None:
        """This method handles the event of the user changing the current selected tab on the TodoList.

        Args:
            e (_type_): _description_
        """
        status_text = self.filter.tabs[self.filter.selected_index].text
        self.status = TaskStatusEnum(status_text)
        self.load_tasks_from_database()
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
            self.on_task_deleted(task)
        self.update()

    def on_name_updated(self) -> None:
        """This method handles the event of the user modifying the name of the Task on the List."""
        self.tasks_repository.update_all([task.model for task in self.tasks.controls])
        self.update()

    def on_description_updated(self) -> None:
        """This method handles the event of the user modifying the description of the Task on the List."""
        self.tasks_repository.update_all([task.model for task in self.tasks.controls])
        self.update()
