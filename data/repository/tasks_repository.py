from enum import Enum
from typing import List

from data.db.database import Database, Session, TasksTable
from data.db.mappers import task_to_tasktable_mapper, tasktable_to_task_mapper
from entity.task import Task


class TaskStatus(Enum):
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

    def update(self, task: Task) -> None:
        with Session(self.database.engine) as session:
            task_orm = session.query(TasksTable).where(TasksTable.id == task.id).one()
            task_orm.name = task.name
            task_orm.description = task.description
            task_orm.completed = task.completed
            session.commit()

    def update_all(self, tasks: List[Task]) -> None:
        with Session(self.database.engine) as session:
            if session.query(TasksTable).count() > 0:
                session.query(TasksTable).delete()

            for task in tasks:
                session.add(task_to_tasktable_mapper(task))
            session.commit()

    def get_by_id(self, task_id: int) -> Task:
        with Session(self.database.engine) as session:
            task = session.query(TasksTable).where(TasksTable.id == task_id).one()
            return map(tasktable_to_task_mapper, task)

    def delete_by_id(self, task_id: int) -> None:
        with Session(self.database.engine) as session:
            task = session.query(TasksTable).get(task_id)
            session.delete(task)
            session.commit()

    def get_all_by_status(self, status=TaskStatus) -> List[Task]:
        with Session(self.database.engine) as session:
            tasks = []

            if status == TaskStatus.all:
                tasks.extend(session.query(TasksTable).all())
            elif status == TaskStatus.active:
                tasks.extend(
                    session.query(TasksTable).where(TasksTable.completed == False).all()
                )
            elif status == TaskStatus.completed:
                tasks.extend(
                    session.query(TasksTable).where(TasksTable.completed == True).all()
                )

            return map(tasktable_to_task_mapper, tasks)
