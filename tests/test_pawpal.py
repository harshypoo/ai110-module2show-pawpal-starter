"""Tests for the PawPal+ core classes."""

from datetime import date, timedelta
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    """A task should be completed after mark_complete is called."""
    task = Task("Morning walk", "07:30", "daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    """Adding a task should increase the number of tasks for that pet."""
    pet = Pet("Biscuit", "dog")
    task = Task("Breakfast", "08:00", "daily")

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_orders_tasks_chronologically() -> None:
    """Tasks with HH:MM times should be returned in chronological order."""
    tasks = [
        Task("Dinner", "18:00", "daily"),
        Task("Breakfast", "08:00", "daily"),
        Task("Morning walk", "07:30", "daily"),
    ]

    sorted_tasks = Scheduler().sort_by_time(tasks)

    assert [task.time for task in sorted_tasks] == ["07:30", "08:00", "18:00"]


def test_sort_by_time_returns_new_stable_order() -> None:
    """Sorting should preserve both the input list and ties' input order."""
    first_eight_am = Task("Breakfast", "08:00", "daily")
    second_eight_am = Task("Medication", "08:00", "daily")
    tasks = [first_eight_am, Task("Morning walk", "07:30", "daily"), second_eight_am]
    original_order = tasks.copy()

    sorted_tasks = Scheduler().sort_by_time(tasks)

    assert tasks == original_order
    assert [task.description for task in sorted_tasks] == [
        "Morning walk",
        "Breakfast",
        "Medication",
    ]


def test_filter_tasks_by_pet_name_and_completion_status() -> None:
    """Filtering can select tasks for a pet, a status, or both together."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat")
    biscuit = Pet("Biscuit", "dog")
    breakfast = Task("Breakfast", "08:00", "daily")
    breakfast.mark_complete()
    mochi.add_task(breakfast)
    biscuit.add_task(Task("Morning walk", "07:30", "daily"))
    owner.add_pet(mochi)
    owner.add_pet(biscuit)
    scheduler = Scheduler()

    assert [task.description for task in scheduler.filter_tasks(owner, pet_name="biscuit")] == [
        "Morning walk"
    ]
    assert [task.description for task in scheduler.filter_tasks(owner, completed=True)] == [
        "Breakfast"
    ]
    assert scheduler.filter_tasks(owner, pet_name="Mochi", completed=False) == []


def test_get_recurring_tasks_filters_daily_and_weekly_tasks() -> None:
    """Recurring-task retrieval excludes one-time and completed tasks."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    pet.add_task(Task("Breakfast", "08:00", "daily"))
    pet.add_task(Task("Brush coat", "10:00", "weekly"))
    pet.add_task(Task("Vet visit", "12:00", "one-time"))
    completed_task = Task("Evening meal", "18:00", "daily")
    completed_task.mark_complete()
    pet.add_task(completed_task)
    owner.add_pet(pet)

    scheduler = Scheduler()

    assert [task.description for task in scheduler.get_recurring_tasks(owner)] == [
        "Breakfast",
        "Brush coat",
    ]
    assert [task.description for task in scheduler.get_recurring_tasks(owner, frequency="weekly")] == [
        "Brush coat"
    ]


def test_detect_conflicts_warns_about_tasks_for_the_same_pet_and_date() -> None:
    """Only duplicate date-and-time slots for one pet should produce a warning."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "cat")
    biscuit = Pet("Biscuit", "dog")
    scheduled_date = date(2026, 10, 11)
    mochi.add_task(Task("Breakfast", "08:00", "daily", scheduled_date=scheduled_date))
    mochi.add_task(Task("Give medication", "08:00", "daily", scheduled_date=scheduled_date))
    mochi.add_task(Task("Tomorrow's breakfast", "08:00", "daily", scheduled_date=date(2026, 10, 12)))
    biscuit.add_task(Task("Morning walk", "08:00", "daily"))
    biscuit.add_task(Task("Lunch", "12:00", "daily"))
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    conflicts = Scheduler().detect_conflicts(owner)

    assert conflicts == [
        "Warning: Mochi has multiple tasks on 2026-10-11 at 08:00: "
        "Breakfast, Give medication."
    ]


def test_detect_conflicts_ignores_completed_tasks() -> None:
    """A completed task should not block an otherwise open care slot."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    completed_task = Task("Breakfast", "08:00", "daily")
    completed_task.mark_complete()
    pet.add_task(completed_task)
    pet.add_task(Task("Give medication", "08:00", "daily"))
    owner.add_pet(pet)

    assert Scheduler().detect_conflicts(owner) == []


def test_completing_recurring_task_creates_next_occurrence() -> None:
    """Daily and weekly tasks should gain a fresh incomplete occurrence."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    daily_task = Task("Breakfast", "08:00", "daily")
    weekly_task = Task("Brush coat", "10:00", "weekly")
    pet.add_task(daily_task)
    pet.add_task(weekly_task)
    owner.add_pet(pet)
    scheduler = Scheduler()

    assert scheduler.complete_task(owner, daily_task.task_id) is True
    assert scheduler.complete_task(owner, weekly_task.task_id) is True

    assert [(task.description, task.frequency, task.completed) for task in pet.tasks] == [
        ("Breakfast", "daily", True),
        ("Brush coat", "weekly", True),
        ("Breakfast", "daily", False),
        ("Brush coat", "weekly", False),
    ]
    assert len({task.task_id for task in pet.tasks}) == 4
    assert pet.tasks[2].scheduled_date == date.today() + timedelta(days=1)
    assert pet.tasks[3].scheduled_date == date.today() + timedelta(weeks=1)


def test_completing_a_recurring_task_twice_creates_only_one_next_occurrence() -> None:
    """Completing an already complete task must not duplicate its recurrence."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    task = Task("Breakfast", "08:00", "daily")
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler()

    assert scheduler.complete_task(owner, task.task_id) is True
    assert scheduler.complete_task(owner, task.task_id) is True
    assert len(pet.tasks) == 2
    assert [task.completed for task in pet.tasks] == [True, False]


def test_completing_one_time_task_does_not_create_another() -> None:
    """One-time tasks should remain completed without being recreated."""
    owner = Owner("Jordan")
    pet = Pet("Biscuit", "dog")
    vet_visit = Task("Vet visit", "12:00", "one-time")
    pet.add_task(vet_visit)
    owner.add_pet(pet)

    assert Scheduler().complete_task(owner, vet_visit.task_id) is True
    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True


def test_completing_an_unknown_task_returns_false_without_changes() -> None:
    """An unknown task ID should not change the owner's existing tasks."""
    owner = Owner("Jordan")
    pet = Pet("Biscuit", "dog")
    task = Task("Morning walk", "07:30", "daily")
    pet.add_task(task)
    owner.add_pet(pet)

    assert Scheduler().complete_task(owner, "missing-task-id") is False
    assert pet.tasks == [task]
    assert task.completed is False


def test_task_normalizes_single_digit_hour() -> None:
    """Accepted times are stored consistently in zero-padded HH:MM format."""
    task = Task("Breakfast", "8:00", "daily")

    assert task.time == "08:00"


@pytest.mark.parametrize("invalid_time", ["24:00", "12:60", "noon"])
def test_task_rejects_invalid_time_formats(invalid_time: str) -> None:
    """Task times must represent valid 24-hour times."""
    with pytest.raises(ValueError, match="24-hour HH:MM"):
        Task("Breakfast", invalid_time, "daily")


@pytest.mark.parametrize(
    ("description", "frequency"),
    [("   ", "daily"), ("Breakfast", "  ")],
)
def test_task_rejects_blank_description_or_frequency(
    description: str, frequency: str
) -> None:
    """A task needs meaningful description and frequency values."""
    with pytest.raises(ValueError):
        Task(description, "08:00", frequency)


def test_get_recurring_tasks_normalizes_frequency_and_rejects_invalid_filter() -> None:
    """Recurring filters accept normalized values but reject unsupported ones."""
    owner = Owner("Jordan")
    pet = Pet("Mochi", "cat")
    pet.add_task(Task("Breakfast", "08:00", "daily"))
    owner.add_pet(pet)
    scheduler = Scheduler()

    assert [task.description for task in scheduler.get_recurring_tasks(owner, frequency=" DAILY ")] == [
        "Breakfast"
    ]
    with pytest.raises(ValueError, match="daily or weekly"):
        scheduler.get_recurring_tasks(owner, frequency="monthly")
