from data.db.database import TasksTable
from entity.task import Task


def tasktable_to_task_mapper(task: TasksTable) -> Task:
    return Task(
        id=task.id,
        name=task.name,
        description=task.description,
        completed=task.completed,
    )
