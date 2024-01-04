import flet as ft

from modules.task import Task


class TodoList(ft.UserControl):
    def build(self):
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
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
                    ],
                ),
            ],
        )

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )
        super().update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def task_status_changed(self):
        self.update()

    def add_clicked(self, e):
        label = self.new_task.value
        if label == "":
            return
        task = Task(
            task_name=label,
            task_status_change=self.task_status_changed,
            task_delete=self.task_delete,
        )
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()

    def tabs_changed(self, e):
        self.update()
