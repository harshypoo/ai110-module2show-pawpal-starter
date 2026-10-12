"""Tests for the PawPal+ core classes."""

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


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
