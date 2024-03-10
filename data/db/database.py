from typing import Any, Callable

import sqlalchemy as db
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class TasksTable(Base):
    """Represents the 'tasks' table in the database.

    Columns:
        id (primary key): int
        name: str(50) (Not Null)
        description: str(255), (Not Null)
        completed: bool (Not Null)
    """

    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    completed = Column(Boolean, nullable=False)


class Database:
    """Represents the Database connection."""

    def __init__(self) -> None:
        """Open the connetion to the <LOCAL> database (SQLITE3).

        This will also create the local database file if it doesn't exist.
        """
        self.engine = create_engine("sqlite:///todolist.db")
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

        self.tasks_table = TasksTable()
        self.create_db()

    def create_db(self) -> None:
        """Ensure that the database exists with given schema."""
        Base.metadata.create_all(self.engine)

    def execute(self, session_processor: Callable) -> None | Any:
        """Execute given database command (session_processor callable)
        and commit to the database.

        Args:
            session_processor (Callable):
                A callable that will be executed withing the database session.

        Returns:
            Any output that the session_processor may return on it's own.
            If there is not return statement, return None.
        """
        with Session(self.engine) as session:
            result = session_processor(session)
            session.commit()
            return result
