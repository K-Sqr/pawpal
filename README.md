# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Architecture (draft UML)

```mermaid
classDiagram
    class Owner {
        +str name
        +list pets
        +add_pet(Pet pet)
        +list_pets()
    }
    class Pet {
        +str name
        +str species
        +list tasks
        +add_task(Task task)
    }
    class Task {
        +str description
        +str time
        +int duration_minutes
        +str priority
        +TaskFrequency frequency
        +bool completed
        +date due_date
        +mark_complete()
    }
    class Scheduler {
        +get_all_tasks_with_pet(Owner owner)
        +tasks_for_date(Owner owner, date on_date)
        +sort_by_time(pairs)
        +filter_tasks(pairs, ...)
        +detect_time_conflicts(pairs)
        +complete_task(Owner, Pet, Task)
    }
    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Scheduler ..> Owner : reads
    Scheduler ..> Task : organizes
```

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
