import flet as ft

from modules.task import Task


class TodoList(ft.UserControl):
    def build(self):
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks = ft.Column()

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
                self.tasks,
            ],
        )

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def add_clicked(self, e):
        label = self.new_task.value
        if label == "":
            return
        task = Task(task_name=label, task_delete=self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.update()
