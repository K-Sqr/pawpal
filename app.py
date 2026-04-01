"""PawPal+ Streamlit UI — wired to pawpal_system logic."""

from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task, TaskFrequency

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

st.title("PawPal+")
st.caption("Smart pet care scheduling — tasks, priorities, and conflict checks.")

with st.expander("About PawPal+", expanded=False):
    st.markdown(
        """
**PawPal+** helps you plan walks, feedings, medications, and appointments. The **Scheduler**
sorts tasks by time, filters by pet or completion, flags same-time conflicts, and rolls recurring
tasks forward when you mark them done.
"""
    )

st.divider()

st.subheader("Owner")
new_owner = st.text_input("Owner name", value=owner.name, key="owner_name_input")
if new_owner.strip():
    owner.name = new_owner.strip()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        pet_name = st.text_input("Pet name", placeholder="Mochi")
    with c2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")
if add_pet and pet_name.strip():
    owner.add_pet(Pet(pet_name.strip(), species))
    st.success(f"Added pet **{pet_name.strip()}** ({species}).")
elif add_pet:
    st.warning("Enter a pet name.")

if owner.pets:
    st.write("Your pets:")
    st.write(", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("Add at least one pet to schedule tasks.")

st.divider()

st.subheader("Tasks")
st.caption("Add a task with a clock time (HH:MM). Choose recurrence for daily or weekly habits.")

if not owner.pets:
    st.warning("Add a pet before creating tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_labels = [p.name for p in owner.pets]
        chosen_pet_name = st.selectbox("Pet", pet_labels)
        title = st.text_input("Task description", value="Morning walk")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            task_time = st.text_input("Time (HH:MM)", value="09:00")
        with tcol2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with pcol2:
            freq_label = st.selectbox("Frequency", ["once", "daily", "weekly"])
        freq_map = {"once": TaskFrequency.ONCE, "daily": TaskFrequency.DAILY, "weekly": TaskFrequency.WEEKLY}
        add_task_btn = st.form_submit_button("Add task")
    if add_task_btn:
        pet_obj = next(p for p in owner.pets if p.name == chosen_pet_name)
        task = Task(
            title.strip() or "Task",
            task_time.strip() or "09:00",
            duration_minutes=int(duration),
            priority=priority,
            frequency=freq_map[freq_label],
            due_date=date.today(),
        )
        pet_obj.add_task(task)
        st.success(f"Scheduled **{task.description}** for **{pet_obj.name}** at {task.time}.")

st.divider()

st.subheader("Today's schedule")
plan_date = st.date_input("Date", value=date.today())
filter_pet = st.selectbox("Filter by pet", ["(all)"] + [p.name for p in owner.pets])
show_completed = st.checkbox("Include completed tasks", value=True)

if st.button("Generate schedule"):
    pairs = scheduler.tasks_for_date(owner, plan_date)
    if not show_completed:
        pairs = scheduler.filter_tasks(pairs, completed=False)
    if filter_pet != "(all)":
        pairs = scheduler.filter_tasks(pairs, pet_name=filter_pet)
    ordered = scheduler.sort_by_time(pairs)
    conflicts = scheduler.detect_time_conflicts(ordered)

    if not ordered:
        st.info("No tasks for this day with the current filters.")
    else:
        rows = []
        for pet, task in ordered:
            rows.append(
                {
                    "Time": task.time,
                    "Pet": pet.name,
                    "Task": task.description,
                    "Duration": task.duration_minutes,
                    "Priority": task.priority,
                    "Done": task.completed,
                    "Why": scheduler.explain_slot(pet, task),
                }
            )
        st.table(rows)
        st.success(f"Showing {len(ordered)} task(s), sorted by time.")

    for msg in conflicts:
        st.warning(msg)

st.divider()

st.subheader("Mark task complete")
if owner.pets:
    all_pairs = scheduler.get_all_tasks_with_pet(owner)
    today_pairs = [(p, t) for p, t in all_pairs if t.due_date == date.today() and not t.completed]
    if today_pairs:
        labels = [f"{p.name} @ {t.time} - {t.description}" for p, t in today_pairs]
        pick = st.selectbox("Choose a pending task (due today)", range(len(labels)), format_func=lambda i: labels[i])
        if st.button("Mark complete"):
            pet_sel, task_sel = today_pairs[pick]
            scheduler.complete_task(owner, pet_sel, task_sel)
            st.success("Marked complete. Recurring tasks get the next occurrence automatically.")
    else:
        st.caption("No pending tasks due today.")
else:
    st.caption("Add pets and tasks first.")
