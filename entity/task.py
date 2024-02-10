from dataclasses import dataclass


@dataclass
class Task:
    name: str
    description: str
    completed: bool
