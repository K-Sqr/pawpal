"""Tests for PawPal+ core behaviors."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task, TaskFrequency


def test_mark_complete_changes_task_status() -> None:
    """Calling mark_complete() sets completed to True."""
    task = Task("Walk", "09:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    """Adding a task to a pet increases that pet's task count."""
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "09:00"))
    pet.add_task(Task("Feed", "18:00"))
    assert len(pet.tasks) == 2


def test_sort_by_time_chronological() -> None:
    """Scheduler returns tasks in chronological order by HH:MM."""
    owner = Owner("A")
    p = Pet("X", "dog")
    owner.add_pet(p)
    today = date(2026, 3, 31)
    p.add_task(Task("Late", "22:00", due_date=today))
    p.add_task(Task("Early", "07:00", due_date=today))
    p.add_task(Task("Noon", "12:30", due_date=today))
    sched = Scheduler()
    pairs = sched.tasks_for_date(owner, today)
    sorted_pairs = sched.sort_by_time(pairs)
    times = [t.time for _, t in sorted_pairs]
    assert times == ["07:00", "12:30", "22:00"]


def test_daily_complete_creates_next_day_task() -> None:
    """Marking a daily task complete adds a new task for the following day."""
    owner = Owner("A")
    pet = Pet("Mochi", "dog")
    owner.add_pet(pet)
    day = date(2026, 6, 1)
    t = Task("Pills", "08:00", frequency=TaskFrequency.DAILY, due_date=day)
    pet.add_task(t)
    sched = Scheduler()
    before = len(pet.tasks)
    sched.complete_task(owner, pet, t)
    assert t.completed is True
    assert len(pet.tasks) == before + 1
    upcoming = [x for x in pet.tasks if not x.completed and x.description == "Pills"]
    assert len(upcoming) == 1
    assert upcoming[0].due_date == day + timedelta(days=1)


def test_detect_time_conflicts_duplicate_clock() -> None:
    """Scheduler flags when two tasks share the same time string."""
    owner = Owner("A")
    pet = Pet("Mochi", "dog")
    owner.add_pet(pet)
    d = date.today()
    pet.add_task(Task("A", "09:00", due_date=d))
    pet.add_task(Task("B", "09:00", due_date=d))
    sched = Scheduler()
    pairs = sched.tasks_for_date(owner, d)
    warnings = sched.detect_time_conflicts(pairs)
    assert len(warnings) >= 1
    assert "09:00" in warnings[0]
