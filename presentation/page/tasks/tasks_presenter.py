from typing import Any

from data.repository.tasks_repository import TasksRepository, TaskStatusEnum
from entity.task import Task


class TasksPresenter:
    tasks_repository: TasksRepository
    view: Any
    task_status_filter_type: TaskStatusEnum

    def __init__(self) -> None:
        self.view = None
        self.task_status_filter_type = TaskStatusEnum.all
        self.tasks_repository = TasksRepository()

    def bind(self, view) -> None:
        self.view = view
        self.update_view()

    def unbind(self) -> None:
        self.view = None

    def update_view(self) -> None:
        if self.view:
            self.view.show_tasks(
                self.tasks_repository.get_all_by_status(self.task_status_filter_type),
                self.get_active_tasks_count(),
            )

    def get_active_tasks_count(self) -> int:
        return len(list(self.tasks_repository.get_all_by_status(TaskStatusEnum.active)))

    def add_task(self, task: Task) -> None:
        self.tasks_repository.insert(task)
        self.update_view()

    def filter_task_by(self, task_status_filter_type: TaskStatusEnum) -> None:
        self.task_status_filter_type = task_status_filter_type
        self.update_view()

    def update_task(self, task: Task) -> None:
        self.tasks_repository.update(task)
        self.update_view()

    def delete_task(self, task) -> None:
        self.tasks_repository.delete_by_id(task.id)
        self.update_view()

    def clear_completed_tasks(self) -> None:
        completed_tasks = self.tasks_repository.get_all_by_status(
            TaskStatusEnum.completed
        )
        for task in completed_tasks:
            self.tasks_repository.delete_by_id(task.id)
        self.update_view()
