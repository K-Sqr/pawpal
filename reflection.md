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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
