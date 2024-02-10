from dataclasses import dataclass


@dataclass
class TaskModel:
    name: str
    description: str
    completed: bool
