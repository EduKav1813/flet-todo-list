from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import sqlalchemy as db

Base = declarative_base()


class TasksTable(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    completed = Column(Boolean, nullable=False)


class Database:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///todolist.db")
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

        self.tasks_table = TasksTable()
        self.create_db()

    def create_db(self) -> None:
        Base.metadata.create_all(self.engine)
