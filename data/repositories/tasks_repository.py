from enum import Enum
from typing import List

from data.db.database import Database, Session, TasksTable
from data.db.mappers import task_to_tasktable_mapper, tasktable_to_task_mapper
from entity.task import Task


class TaskStatusEnum(Enum):
    all = "all"
    active = "active"
    completed = "completed"


class TasksRepository:
    def __init__(self) -> None:
        self.database = Database()

    def insert(self, task: Task) -> None:
        with Session(self.database.engine) as session:
            session.add(task_to_tasktable_mapper(task))
            session.commit()

    def update_all(self, tasks: List[Task]) -> None:
        with Session(self.database.engine) as session:
            if session.query(TasksTable).count() > 0:
                session.query(TasksTable).delete()

            for task in tasks:
                session.add(task_to_tasktable_mapper(task))
            session.commit()

    def delete_by_id(self, task_id: int) -> None:
        with Session(self.database.engine) as session:
            task = session.query(TasksTable).get(task_id)
            session.delete(task)
            session.commit()

    def get_all_by_status(self, status=TaskStatusEnum) -> List[Task]:
        with Session(self.database.engine) as session:
            tasks = []

            if status == TaskStatusEnum.all:
                tasks.extend(session.query(TasksTable).all())
            elif status == TaskStatusEnum.active:
                tasks.extend(
                    session.query(TasksTable).where(TasksTable.completed == False).all()
                )
            elif status == TaskStatusEnum.completed:
                tasks.extend(
                    session.query(TasksTable).where(TasksTable.completed == True).all()
                )

            return map(tasktable_to_task_mapper, tasks)
