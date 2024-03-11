from typing import Callable

import flet as ft

from entity.task import Task


class TaskComponent(ft.UserControl):
    def __init__(
        self,
        model: Task,
        on_task_update: Callable,
        on_task_delete: Callable,
    ):
        super().__init__()
        # Values held by the task
        self.model = model

        # Methods from TodoList that will be called on their respective actions:
        self.on_task_update = on_task_update
        self.on_task_delete = on_task_delete

    def build(self):
        self.display_task = ft.Checkbox(
            value=self.model.completed,
            label=self.model.name,
            on_change=self.on_status_changed,
        )
        self.edit_name = ft.TextField(expand=1)

        self.description_label = ft.Text(
            self.model.description,
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
                            on_click=self.on_edit_name_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=lambda e: self.on_task_delete(self),
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
                    on_click=self.on_save_name_clicked,
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
                    on_click=self.on_edit_description_clicked,
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
                    on_click=self.on_save_description_clicked,
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

    def on_edit_name_clicked(self, e) -> None:
        """Opens the name-edit-view for the user to change the name of the task.
        Other edit views may be opened in parallel, like description-edit-view.
        """
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_name_view.visible = True
        self.update()

    def on_edit_description_clicked(self, e) -> None:
        """Opens the description-edit-view for the user to change the description of the task.
        Other edit views may be opened in parallel, like name-edit-view.
        """
        self.edit_description.value = self.model.description
        self.description_view.visible = False
        self.edit_description_view.visible = True
        self.update()

    def on_save_name_clicked(self, e) -> None:
        """Concludes the process of modifying the name of this Task.
        The typed text in the text field is saved as the new task name,
        and name modifying view is closed.
        Default view of the Task is opened.

        Will also call respective update function from the TodoList.
        """
        self.model.name = self.edit_name.value
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_name_view.visible = False
        self.update()
        self.on_task_update(self)

    def on_save_description_clicked(self, e) -> None:
        """Concludes the process of modifying the description of this Task.
        The typed text in the text field is saved as the new task description,
        and description modifying view is closed.
        Default view of the Task is opened.

        Will also call respective update function from the TodoList.
        """
        self.model.description = str(self.edit_description.value).strip()
        self.description_label.value = self.model.description
        self.description_view.visible = True
        self.edit_description_view.visible = False
        self.update()
        self.on_task_update(self)

    def on_status_changed(self, e) -> None:
        """Event handler for when the status of the task is changed.

        Will also call respective update function from the TodoList.
        """
        self.model.completed = self.display_task.value
        self.on_task_update(self)
