from data.db.database import TasksTable
from entity.task import Task


def task_to_tasktable_mappper(task: Task) -> TasksTable:
    return TasksTable(
        name=task.name, description=task.description, completed=task.completed
    )
