from typing import List

import flet as ft

from data.repository.tasks_repository import TaskStatus
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
                ft.Tab(text=TaskStatus.ALL.value),
                ft.Tab(text=TaskStatus.ACTIVE.value),
                ft.Tab(text=TaskStatus.COMPLETED.value),
            ],
        )

        self.status = TaskStatus.ALL
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
                on_task_update=self.on_task_update,
                on_task_delete=self.on_task_delete,
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
        """
        label = self.new_task.value
        self.new_task.value = ""

        if label == "":
            return

        self.presenter.add_task(
            Task(id=None, name=label, description="Details", completed=False)
        )

    def bind_tabs_changed(self, e) -> None:
        """This method handles the event of the user changing the current selected tab on the TodoList."""
        status = TaskStatus(self.filter.tabs[self.filter.selected_index].text)
        self.presenter.filter_task_by(status)

    def clear_clicked(self, e) -> None:
        """This method handles the even of the clicking the 'Clear' button.
        This button clears all tasks that are in the 'completed' state.
        Tasks that are 'active' will remain on the list.
        """
        self.presenter.clear_completed_tasks()

    ## Callbacks to TaskComponent
    def on_task_update(self, task: TaskComponent) -> None:
        """Called on any TaskComponent update

        Args:
            task (TaskComponent): TaskComponent instance that triggered the update.
        """
        self.presenter.update_task(task.model)

    def on_task_delete(self, task: TaskComponent) -> None:
        """Remove the given task from the TodoList

        Args:
            task (TaskComponent): TaskComponent instance that triggered deletion.
        """
        self.presenter.delete_task(task.model)
