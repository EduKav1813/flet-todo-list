import flet as ft

from modules.task import Task
from modules.db import Database, TasksTable, Session


class TodoList(ft.UserControl):
    def build(self):
        self.items_left = ft.Text()
        self.update_active_items_left(0)
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()
        self.database = Database()
        self.load_tasks_from_database()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
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
        with Session(self.database.engine) as session:
            if session.query(TasksTable).count() > 0:
                session.query(TasksTable).delete()

            for task in self.tasks.controls:
                new_task = TasksTable(
                    name=task.task_name,
                    description=task.description,
                    completed=task.completed,
                )
                session.add(new_task)

            session.commit()

    def load_tasks_from_database(self) -> None:
        with Session(self.database.engine) as session:
            if session.query(TasksTable).count() > 0:
                tasks = session.query(TasksTable).all()
                for task in tasks:
                    new_task = Task(
                        task_name=task.name,
                        description=task.description,
                        completed=task.completed,
                        task_status_change=self.task_status_changed,
                        task_delete=self.task_delete,
                        description_updated=self.description_updated,
                    )
                    self.tasks.controls.append(new_task)


    def update_active_items_left(self, tasks_left: int):
        self.items_left.value = f"{tasks_left} active item(s) left"

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )

        tasks_left_count = [task.completed for task in self.tasks.controls].count(False)
        self.update_active_items_left(tasks_left_count)
        self.update_database()

        super().update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()
        self.update_database()

    def task_status_changed(self):
        self.update()
        self.update_database()

    def add_clicked(self, e):
        label = self.new_task.value
        if label == "":
            return
        task = Task(
            task_name=label,
            description="Details",
            completed=False,
            task_status_change=self.task_status_changed,
            task_delete=self.task_delete,
            description_updated=self.description_updated,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()
        self.update_database()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        completed_tasks = [task for task in self.tasks.controls if task.completed]
        for task in completed_tasks:
            self.task_delete(task)
        self.update()
        self.update_database()

    def description_updated(self):
        self.update()
        self.update_database()
