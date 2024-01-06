import flet as ft


class Task(ft.UserControl):
    def __init__(
        self,
        task_name,
        description,
        completed,
        task_status_change,
        task_delete,
        description_updated,
    ):
        super().__init__()
        self.completed = completed
        self.task_name = task_name
        self.description = description
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.description_updated = description_updated

    def delete_clicked(self, e):
        self.task_delete(self)

    def build(self):
        self.display_task = ft.Checkbox(
            value=self.completed, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.description_label = ft.Text(
            self.description,
            max_lines=3,
            selectable=True,
            overflow="ellipsis",
            width=450,
        )
        self.edit_description = ft.TextField(expand=1, max_lines=5, multiline=True)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_name_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_name_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_name_clicked,
                ),
            ],
        )

        self.description_view = ft.Row(
            visible=True,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.description_label,
                ft.IconButton(
                    icon=ft.icons.CREATE_OUTLINED,
                    tooltip="Edit Description",
                    on_click=self.edit_description_clicked,
                ),
            ],
        )

        self.edit_description_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_description,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update Description",
                    on_click=self.save_description_clicked,
                ),
            ],
        )
        return ft.Column(
            controls=[
                self.display_view,
                self.edit_name_view,
                self.description_view,
                self.edit_description_view,
            ]
        )

    def edit_name_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_name_view.visible = True
        self.update()

    def edit_description_clicked(self, e):
        self.edit_description.value = self.description
        self.description_view.visible = False
        self.edit_description_view.visible = True
        self.update()

    def save_name_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_name_view.visible = False
        self.update()

    def save_description_clicked(self, e):
        self.description = self.edit_description.value
        self.description_label.value = self.description
        self.description_view.visible = True
        self.edit_description_view.visible = False
        self.update()
        self.description_updated()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change()