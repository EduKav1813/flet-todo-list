from enum import Enum
from typing import Iterable, List

from data.db.database import Database, TasksTable
from data.db.mappers import task_to_tasktable_mapper, tasktable_to_task_mapper
from entity.task import Task


class TaskStatus(Enum):
    ALL = "all"
    ACTIVE = "active"
    COMPLETED = "completed"


class TasksRepository:
    def __init__(self) -> None:
        self.database = Database()

    def insert(self, task: Task) -> None:
        def session_processor(session) -> None:
            session.add(task_to_tasktable_mapper(task))

        self.database.execute(session_processor)

    def update(self, task: Task) -> None:
        def session_processor(session) -> None:
            task_orm = session.query(TasksTable).where(TasksTable.id == task.id).one()
            task_orm.name = task.name
            task_orm.description = task.description
            task_orm.completed = task.completed

        self.database.execute(session_processor)

    def update_all(self, tasks: List[Task]) -> None:
        def session_processor(session) -> None:
            if session.query(TasksTable).count() > 0:
                session.query(TasksTable).delete()

            for task in tasks:
                session.add(task_to_tasktable_mapper(task))

        self.database.execute(session_processor)

    def get_by_id(self, task_id: int) -> Task:
        def session_processor(session) -> Iterable:
            task = session.query(TasksTable).where(TasksTable.id == task_id).one()
            return map(tasktable_to_task_mapper, task)

        return self.database.execute(session_processor)

    def delete_by_id(self, task_id: int) -> None:
        def session_processor(session) -> None:
            task = session.query(TasksTable).get(task_id)
            session.delete(task)

        self.database.execute(session_processor)

    def get_all_by_status(self, status=TaskStatus) -> List[Task]:
        def session_processor(session) -> Iterable:
            tasks = []

            if status == TaskStatus.ALL:
                tasks.extend(session.query(TasksTable).all())
            elif status == TaskStatus.ACTIVE:
                tasks.extend(
                    session.query(TasksTable).where(TasksTable.completed == False).all()
                )
            elif status == TaskStatus.COMPLETED:
                tasks.extend(
                    session.query(TasksTable).where(TasksTable.completed == True).all()
                )

            return map(tasktable_to_task_mapper, tasks)

        return self.database.execute(session_processor)
