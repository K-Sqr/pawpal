# PawPal+ Project Reflection

## System Design — three core user actions

1. **Register pets and care context** — Add an owner profile and one or more pets (name, species) so all tasks are tied to a real animal.
2. **Schedule and maintain tasks** — Create care tasks with a time, priority, duration, and optional recurrence (daily/weekly) so feedings, walks, medications, and appointments stay organized.
3. **See today’s plan** — View a clear schedule for a chosen day: tasks sorted by time, optional filters, and warnings if two items collide at the same clock time.

---

## 1. System Design

**a. Initial design**

- The UML centers on four types: **Owner** (has many **Pet**), **Pet** (has many **Task**), and **Scheduler** (reads tasks through the owner’s pets, orders and filters them, and reports conflicts). **Task** holds description, clock time (`HH:MM`), duration, priority, frequency (`once` / `daily` / `weekly`), completion flag, and a due date for calendar-day filtering and recurrence.
- **Owner** stores identity and a list of pets; **Pet** stores identity and its task list. **Scheduler** does not own data; it aggregates `(Pet, Task)` pairs, sorts by time, filters by pet name or completion, detects same-time conflicts, and completes tasks while spawning the next occurrence for recurring items.

**b. Design changes**

- The skeleton listed convenience methods like `list_pets()` on paper; the implementation keeps `Owner.pets` as a simple list and iterates directly, which avoided extra API surface while staying clear.
- Recurrence handling lives in `Scheduler.complete_task` plus `Task.clone_for_next_occurrence` so the UI and CLI both go through one code path instead of duplicating date math on `Task` alone.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers **calendar due date** (which tasks belong to the selected day), **clock time** (for ordering), **duration** and **priority** (surfaced in `explain_slot` for transparency), and **completion status** (filtering). The strongest structural constraint is **date** (today’s plan), then **time order** for the displayed list. Priority is informational in this version rather than a reordering rule, so the owner still sees a time-ordered day while reading why each row matters.

**b. Tradeoffs**

- **Conflict detection** only flags tasks that share the **exact same `HH:MM` string**. It does not detect overlapping intervals when two long tasks run across each other at different start times. That keeps the implementation small and predictable for a course scope; a production app might store start/end datetimes or durations and check interval overlap instead.

---

## 3. AI Collaboration

**a. How you used AI**

- AI was useful for structuring the work into phases (UML first, CLI second, UI third), suggesting dataclasses and a Scheduler that reads through `Owner` instead of holding global state, and drafting pytest cases for sorting, recurrence, and conflicts. **Copilot-style** inline prompts on a specific method (for example `sort_by_time`) were faster than broad chat when the surrounding types were already fixed. The most helpful prompts were concrete and file-scoped (for example: given `Task.time` as `HH:MM`, how should the sort key work?) rather than open-ended requests to write the entire app. Using **separate chat sessions per phase** (design vs algorithms vs tests) reduced context mixing and kept each thread focused on one layer of the system.

**b. Judgment and verification**

- One suggestion was to use Unicode arrows and symbols in CLI output for a polished look. On Windows default consoles that can raise encoding errors, so the implementation was adjusted to ASCII-only output in `main.py` and `explain_slot`, verified by running `python main.py` locally. The design stayed the same; only the presentation layer changed after a runtime check.

---

## 4. Testing and Verification

**a. What you tested**

- Tests cover task completion, pet task list growth, chronological sort for mixed times, daily recurrence after `complete_task`, and conflict detection for duplicate clock times. These guard behaviors users rely on: ordering the day, not losing recurring work, and surfacing warnings instead of silent overlaps.

**b. Confidence**

- Confidence: 4/5 (aligned with the README). With more time, next tests would include weekly recurrence across month boundaries, invalid `HH:MM` input, pets with zero tasks, and marking complete when the same description appears twice.

---

## 5. Reflection

**a. What went well**

- The split between data (`Owner`, `Pet`, `Task`) and behavior (`Scheduler`) stayed stable from UML to Streamlit and made the CLI demo trustworthy before wiring the UI.

**b. What you would improve**

- Add priority-aware scheduling (not only time order), validation for time strings, and interval-based overlap for conflicts instead of exact clock matches.

**c. Key takeaway**

- Being the lead architect means owning the boundaries: AI can speed up scaffolding and tests, but you decide API shape, persistence (`session_state`), and which tradeoffs (like exact-time conflicts) are acceptable for the product scope.
