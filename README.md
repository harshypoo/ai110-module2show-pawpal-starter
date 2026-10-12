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

## Features

- **Time-based sorting:** Orders validated `HH:MM` task times chronologically with `Scheduler.sort_by_time()`.
- **Flexible filtering:** Shows tasks by pet, completion status, or both through `Scheduler.filter_tasks()`.
- **Conflict warnings:** Detects incomplete tasks for the same pet that share a date-and-time slot, then returns a clear warning instead of stopping the app.
- **Recurring care:** Identifies daily and weekly tasks. Completing one creates a fresh incomplete occurrence for tomorrow or the following week; one-time tasks are not recreated.
- **Completion tracking:** Lets an owner mark care tasks complete while retaining the completed task in history.
- **Date-aware task management:** Stores a scheduled date with every task so tasks at the same time on different dates do not conflict.
- **Streamlit task planner:** Lets an owner create pets and tasks, filter the displayed plan, review recurring care, see conflict warnings, and complete tasks in the browser session.

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

## 🖥️ Sample Output

Run `python main.py` to see a terminal demonstration of task sorting, filtering, and conflict warnings. A representative output is included in the demo walkthrough below.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```
python -m pytest
This command runs the test suite that covers all happy cases such as sorting correctly,
daily and weekly tasks creating a new instance if completed, one-time tasks not recurring,
conflicts being detected, and recurring tasks being filtered. It also includes edge cases
such as equal-time sorting, complete a recurring task twice does not create duplicates,
completed tasks do not count as conflicts, unkown tasks are False, invalid times are errors,
and frequency filters handle extra space or reject unsupported values.
```
============================================================ test session starts ============================================================
platform darwin -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/harshpatel/Desktop/AI110/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 19 items                                                                                                                          

tests/test_pawpal.py ...................                                                                                              [100%]

============================================================ 19 passed in 0.02s =============================================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time() | Uses sorted method and lambda to validate by HH:MM |
| Filtering | Scheduler.filter_tasks() | Filters tasks by copmletion status, pet name, or both. |
| Conflict handling | Scheduler.detect_conflicts() | Displays warning message when same pet has multiple 
incomplete tasks on same day and time. Different pets or dates do not conflict. |
| Recurring tasks | Task.is_recurring() and Task.create_next_occurence() and Scheduler.get_recurring_tasks() 
and Scheduler.complete_task() | Daily and weekly tasks new instance after completion unless it's one-time. |

## Implementation Summary
The app now has all the logic implemented to include Task, Pet, Owner, and Scheduler objects. Task represents
one task for the pet with a description, time, frequency, completion status, ID, and the pet's name.
The Pet is the actual pet's information and task list. Owner is the person managing the pets. Scheduler
is the planning brain that helps the owner organize all tasks, retrieve all tasks, sort, and get a schedule.
All of these come together to organize all tasks that the owner wants for a specific pet.

## 📸 Demo Walkthrough

The Streamlit app lets a pet owner create or select an owner, add pets, schedule dated care tasks, filter the task list, review recurring tasks, resolve warnings, and mark tasks complete. Completing a daily or weekly task automatically creates its next occurrence.

Example workflow:

1. Create or select an owner, then add a pet such as Mochi.
2. Add a task by choosing the pet, entering a description, selecting a date and time, and choosing daily, weekly, or one-time frequency.
3. Use the pet and completion-status controls to view the relevant tasks in a chronological table.
4. Review recurring tasks and any warning displayed when one pet has more than one incomplete task at the same date and time.
5. Select Mark complete for a task. The app keeps it in history and creates the next daily or weekly occurrence when applicable.

The terminal demo shows the same scheduler behaviors: tasks are sorted from earliest to latest, filtering can isolate Biscuit's or completed tasks, and a duplicate Mochi time slot produces a non-blocking warning.

```
Tasks as entered
================
17:30 — Mochi: Playtime (complete)
08:00 — Mochi: Breakfast (incomplete)
08:00 — Mochi: Give medication (incomplete)
20:00 — Biscuit: Medication (incomplete)
07:30 — Biscuit: Morning walk (incomplete)

Sorted by time
==============
07:30 — Biscuit: Morning walk (incomplete)
08:00 — Mochi: Breakfast (incomplete)
08:00 — Mochi: Give medication (incomplete)
17:30 — Mochi: Playtime (complete)
20:00 — Biscuit: Medication (incomplete)

Biscuit's tasks
===============
20:00 — Biscuit: Medication (incomplete)
07:30 — Biscuit: Morning walk (incomplete)

Completed tasks
===============
17:30 — Mochi: Playtime (complete)

Today's incomplete schedule
===========================
07:30 — Biscuit: Morning walk (incomplete)
08:00 — Mochi: Breakfast (incomplete)
08:00 — Mochi: Give medication (incomplete)
20:00 — Biscuit: Medication (incomplete)

Schedule warnings
=================
Warning: Mochi has multiple tasks on 2026-10-11 at 08:00: Breakfast, Give medication.
```