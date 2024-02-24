from dataclasses import dataclass
from typing import List

from entity.task import Task


@dataclass
class TasksPageState:
    tasks: List[Task]
    active_tasks_count: int
