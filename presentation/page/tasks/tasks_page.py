from typing import List

import flet as ft

from data.repository.tasks_repository import TaskStatusEnum
from data.state.tasks_page_state import TasksPageState
from entity.task import Task
from presentation.component.task_component import TaskComponent
from presentation.page.tasks.tasks_presenter import TasksPresenter


class TasksPage(ft.UserControl):
    def __init__(self, presenter: TasksPresenter, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.page_state = TasksPageState([], 0)
        self.presenter = presenter

        # UI Components
        self.tasks = ft.Column()

    def build(self):
        self.items_left = ft.Text()
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)

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

    def fill_tasks(self) -> None:
        self.tasks.clean()
        for task in self.page_state.tasks:
            task_component = TaskComponent(
                model=task,
                on_task_status_changed=self.on_task_status_changed,
                on_task_deleted=self.on_task_deleted,
                on_name_updated=self.on_name_updated,
                on_description_updated=self.on_description_updated,
            )
            self.tasks.controls.append(task_component)

    def update(self):
        self.update_active_items_left()
        super().update()

    def update_active_items_left(self) -> None:
        """Method to update the 'active items left' label."""
        self.items_left.value = (
            f"{self.page_state.active_tasks_count} active item(s) left"
        )

    def show_tasks(self, tasks: List[Task], active_tasks_count: int) -> None:
        self.page_state = TasksPageState(tasks, active_tasks_count)
        self.fill_tasks()
        self.update()

    def add_clicked(self, e) -> None:
        """This method handles adding the new task in the TodoList, when user clicks the 'Add' button.

        If the Task name is empty, task will not be created.

        Args:
            e (_type_): _description_
        """
        label = self.new_task.value
        self.new_task.value = ""

        if label == "":
            return

        self.presenter.add_task(
            Task(id=None, name=label, description="Details", completed=False)
        )

    def bind_tabs_changed(self, e) -> None:
        """This method handles the event of the user changing the current selected tab on the TodoList.

        Args:
            e (_type_): _description_
        """
        status = TaskStatusEnum(self.filter.tabs[self.filter.selected_index].text)
        self.presenter.filter_task_by(status)

    def clear_clicked(self, e) -> None:
        """This method handles the even of the clicking the 'Clear' button.
        This button clears all tasks that are in the 'completed' state.
        Tasks that are 'active' will remain on the list.

        Args:
            e (_type_): _description_
        """
        self.presenter.clear_completed_tasks()
        self.update()

    ## Callbacks to TaskComponent
    def on_name_updated(self, task: TaskComponent) -> None:
        """This method handles the event of the user modifying the name of the Task on the List."""
        self.presenter.update_task(task.model)

    def on_description_updated(self, task: TaskComponent) -> None:
        """This method handles the event of the user modifying the description of the Task on the List."""
        self.presenter.update_task(task.model)

    def on_task_status_changed(self, task: TaskComponent) -> None:
        """This method handles the event when the status of the Task in the TodoList was changed."""
        self.presenter.update_task(task.model)

    def on_task_deleted(self, task: TaskComponent) -> None:
        """Remove the given task from the TodoList

        Args:
            task (Task): Task to delete.
        """
        self.presenter.delete_task(task.model)
