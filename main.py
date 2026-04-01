"""CLI demo for PawPal+ — verify logic before the Streamlit UI."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task, TaskFrequency


def format_schedule_heading(on_date: date) -> str:
    """Return a readable title for the schedule block."""
    return f"Today's Schedule - {on_date.isoformat()}"


def main() -> None:
    today = date.today()
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added out of chronological order on purpose (sorting demo).
    mochi.add_task(
        Task("Evening walk", "18:30", duration_minutes=25, priority="medium", due_date=today)
    )
    mochi.add_task(
        Task("Morning walk", "07:15", duration_minutes=20, priority="high", due_date=today)
    )
    luna.add_task(
        Task("Breakfast", "08:00", duration_minutes=10, priority="high", due_date=today)
    )
    mochi.add_task(
        Task("Heart medication", "08:00", duration_minutes=5, priority="high", due_date=today)
    )

    scheduler = Scheduler()
    raw = scheduler.tasks_for_date(owner, today)
    ordered = scheduler.sort_by_time(raw)

    print(format_schedule_heading(today))
    print("-" * 48)
    for pet, task in ordered:
        line = (
            f"{task.time}  |  {pet.name} ({pet.species})  |  {task.description}  "
            f"[{task.priority}]  ({task.duration_minutes} min)"
        )
        print(line)
        print(f"         -> {scheduler.explain_slot(pet, task)}")
    print("-" * 48)

    conflicts = scheduler.detect_time_conflicts(ordered)
    if conflicts:
        print("Time conflict warnings:")
        for w in conflicts:
            print(f"  WARNING: {w}")
    else:
        print("No same-time conflicts detected.")

    # Filtering demo: pending tasks only.
    pending = scheduler.filter_tasks(ordered, completed=False)
    print(f"\nPending tasks today: {len(pending)}")

    # Recurring demo: mark a daily task complete and show new instance.
    daily = Task(
        "Water bowl refill",
        "12:00",
        frequency=TaskFrequency.DAILY,
        due_date=today,
    )
    mochi.add_task(daily)
    scheduler.complete_task(owner, mochi, daily)
    next_days = [t for t in mochi.tasks if t.description == "Water bowl refill" and not t.completed]
    if next_days:
        n = next_days[0]
        print(
            f"\nAfter completing daily task, next occurrence due on {n.due_date.isoformat()} "
            f"at {n.time}."
        )


if __name__ == "__main__":
    main()
