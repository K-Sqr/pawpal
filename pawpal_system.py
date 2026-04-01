"""PawPal+ logic layer — Owner, Pet, Task, and Scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional, Tuple


class TaskFrequency(str, Enum):
    """How often a task repeats."""

    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


def _time_sort_key(time_str: str) -> Tuple[int, int]:
    """Parse 'HH:MM' into a tuple for stable chronological ordering."""
    parts = time_str.strip().split(":")
    h = int(parts[0]) if parts else 0
    m = int(parts[1]) if len(parts) > 1 else 0
    return (h, m)


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
        self.completed = True

    def clone_for_next_occurrence(self) -> Task:
        """Create the next recurring instance after completion."""
        if self.frequency == TaskFrequency.ONCE:
            return replace(self)
        if self.frequency == TaskFrequency.DAILY:
            return replace(
                self,
                completed=False,
                due_date=self.due_date + timedelta(days=1),
            )
        if self.frequency == TaskFrequency.WEEKLY:
            return replace(
                self,
                completed=False,
                due_date=self.due_date + timedelta(weeks=1),
            )
        return replace(self)


@dataclass
class Pet:
    """A pet belonging to an owner; holds its care tasks."""

    name: str
    species: str = "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """A person who owns one or more pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)


class Scheduler:
    """Aggregates and organizes tasks across an owner's pets."""

    def get_all_tasks_with_pet(self, owner: Owner) -> List[Tuple[Pet, Task]]:
        """Return (pet, task) pairs for every task under the owner."""
        pairs: List[Tuple[Pet, Task]] = []
        for pet in owner.pets:
            for task in pet.tasks:
                pairs.append((pet, task))
        return pairs

    def tasks_for_date(self, owner: Owner, on_date: date) -> List[Tuple[Pet, Task]]:
        """Tasks due on a given calendar day."""
        out: List[Tuple[Pet, Task]] = []
        for pet, task in self.get_all_tasks_with_pet(owner):
            if task.due_date == on_date:
                out.append((pet, task))
        return out

    def sort_by_time(self, pairs: List[Tuple[Pet, Task]]) -> List[Tuple[Pet, Task]]:
        """Sort tasks by scheduled time (HH:MM)."""
        return sorted(pairs, key=lambda pt: _time_sort_key(pt[1].time))

    def filter_tasks(
        self,
        pairs: List[Tuple[Pet, Task]],
        *,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Tuple[Pet, Task]]:
        """Filter by pet name and/or completion status."""
        result = list(pairs)
        if pet_name is not None:
            pn = pet_name.strip().lower()
            result = [(p, t) for p, t in result if p.name.lower() == pn]
        if completed is not None:
            result = [(p, t) for p, t in result if t.completed == completed]
        return result

    def detect_time_conflicts(self, pairs: List[Tuple[Pet, Task]]) -> List[str]:
        """Return human-readable warnings when multiple tasks share the same time."""
        by_time: dict[str, List[Tuple[Pet, Task]]] = {}
        for pet, task in pairs:
            key = task.time.strip()
            by_time.setdefault(key, []).append((pet, task))
        warnings: List[str] = []
        for tkey, group in by_time.items():
            if len(group) < 2:
                continue
            labels = [f"{p.name}: {tsk.description}" for p, tsk in group]
            warnings.append(
                f"Conflict at {tkey}: " + "; ".join(labels)
            )
        return warnings

    def complete_task(self, owner: Owner, pet: Pet, task: Task) -> None:
        """Mark a task complete and enqueue the next occurrence if recurring."""
        if pet not in owner.pets:
            raise ValueError("Pet does not belong to this owner.")
        if task not in pet.tasks:
            raise ValueError("Task is not on this pet's list.")
        task.mark_complete()
        if task.frequency != TaskFrequency.ONCE:
            nxt = task.clone_for_next_occurrence()
            pet.add_task(nxt)

    def explain_slot(self, pet: Pet, task: Task) -> str:
        """One-line rationale for display (priority + duration)."""
        return (
            f"{task.description} for {pet.name} - {task.time}, "
            f"{task.duration_minutes} min, {task.priority} priority"
        )
