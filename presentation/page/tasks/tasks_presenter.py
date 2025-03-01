from typing import Any

from data.repository.tasks_repository import TasksRepository, TaskStatus
from entity.task import Task
from presentation.base_presenter import BasePresenter


class TasksPresenter(BasePresenter):
    tasks_repository: TasksRepository
    task_status_filter_type: TaskStatus

    def __init__(self) -> None:
        super().__init__()
        self.task_status_filter_type = TaskStatus.ALL
        self.tasks_repository = TasksRepository()

    def bind(self, view) -> None:
        super().bind(view)
        self.show_tasks()

    def show_tasks(self) -> None:
        if self.view:
            self.view.show_tasks(
                self.tasks_repository.get_all_by_status(self.task_status_filter_type),
                self.get_active_tasks_count(),
            )

    def get_active_tasks_count(self) -> int:
        return len(self.tasks_repository.get_all_by_status(TaskStatus.ACTIVE))

    def add_task(self, task: Task) -> None:
        self.tasks_repository.insert(task)
        self.show_tasks()

    def filter_task_by(self, task_status_filter_type: TaskStatus) -> None:
        self.task_status_filter_type = task_status_filter_type
        self.show_tasks()

    def update_task(self, task: Task) -> None:
        self.tasks_repository.update(task)
        self.show_tasks()

    def delete_task(self, task) -> None:
        self.tasks_repository.delete_by_id(task.id)
        self.show_tasks()

    def clear_completed_tasks(self) -> None:
        completed_tasks = self.tasks_repository.get_all_by_status(TaskStatus.COMPLETED)
        for task in completed_tasks:
            self.tasks_repository.delete_by_id(task.id)
        self.show_tasks()
