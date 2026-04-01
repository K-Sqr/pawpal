"""PawPal+ logic layer — class skeletons derived from UML."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional, Tuple


class TaskFrequency(str, Enum):
    """How often a task repeats."""

    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Task:
    """A single care activity for a pet."""

    description: str
    time: str
    duration_minutes: int = 30
    priority: str = "medium"
    frequency: TaskFrequency = TaskFrequency.ONCE
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def clone_for_next_occurrence(self) -> Task:
        """Create the next recurring instance after completion."""
        pass


@dataclass
class Pet:
    """A pet belonging to an owner; holds its care tasks."""

    name: str
    species: str = "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        pass


@dataclass
class Owner:
    """A person who owns one or more pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        pass


class Scheduler:
    """Aggregates and organizes tasks across an owner's pets."""

    def get_all_tasks_with_pet(self, owner: Owner) -> List[Tuple[Pet, Task]]:
        """Return (pet, task) pairs for every task under the owner."""
        pass

    def tasks_for_date(self, owner: Owner, on_date: date) -> List[Tuple[Pet, Task]]:
        """Tasks due on a given calendar day."""
        pass

    def sort_by_time(self, pairs: List[Tuple[Pet, Task]]) -> List[Tuple[Pet, Task]]:
        """Sort tasks by scheduled time (HH:MM)."""
        pass

    def filter_tasks(
        self,
        pairs: List[Tuple[Pet, Task]],
        *,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Tuple[Pet, Task]]:
        """Filter by pet name and/or completion status."""
        pass

    def detect_time_conflicts(self, pairs: List[Tuple[Pet, Task]]) -> List[str]:
        """Return human-readable warnings when multiple tasks share the same time."""
        pass

    def complete_task(self, owner: Owner, pet: Pet, task: Task) -> None:
        """Mark a task complete and enqueue the next occurrence if recurring."""
        pass
