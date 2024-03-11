from data.db.database import TasksTable
from entity.task import Task


def task_to_tasktable_mapper(task: Task) -> TasksTable:
    return TasksTable(
        id=task.id,
        name=task.name,
        description=task.description,
        completed=task.completed,
    )
