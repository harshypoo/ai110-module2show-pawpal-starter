"""Core models and scheduling logic for the PawPal+ pet-care planner."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    """A single care activity assigned to a pet."""

    description: str
    time: str
    frequency: str
    completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid4()))
    pet_name: str | None = None

    def __post_init__(self) -> None:
        """Normalize task text and ensure the scheduled time is usable."""
        self.description = self.description.strip()
        self.frequency = self.frequency.lower().strip()
        if not self.description:
            raise ValueError("A task needs a description.")
        if not self.frequency:
            raise ValueError("A task needs a frequency.")

        try:
            self.time = datetime.strptime(self.time, "%H:%M").strftime("%H:%M")
        except ValueError as error:
            raise ValueError("time must use 24-hour HH:MM format.") from error

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False


@dataclass
class Pet:
    """Stores pet details and the care tasks assigned to that pet."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add one care task to this pet."""
        if any(existing.task_id == task.task_id for existing in self.tasks):
            raise ValueError("This task is already assigned to the pet.")
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID and report whether it was found."""
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return True
        return False

    def get_tasks(self) -> list[Task]:
        """Return a copy of this pet's tasks."""
        return self.tasks.copy()


@dataclass
class Owner:
    """Manages multiple pets and provides access to their combined tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care."""
        if all(existing is not pet for existing in self.pets):
            self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove the first pet with the given name, if present."""
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                return True
        return False

    def get_all_tasks(self) -> list[Task]:
        """Return tasks from every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.get_tasks()]


@dataclass
class Scheduler:
    """The planning brain that retrieves and organizes tasks across pets."""

    schedule: list[Task] = field(default_factory=list, init=False)

    def retrieve_tasks(self, owner: Owner) -> list[Task]:
        """Retrieve every task through the owner's combined-task method."""
        return owner.get_all_tasks()

    def organize_tasks(self, owner: Owner) -> list[Task]:
        """Return incomplete tasks ordered by their scheduled time."""
        tasks = self.retrieve_tasks(owner)
        return sorted(
            (task for task in tasks if not task.completed),
            key=lambda task: (task.time, task.description.lower()),
        )

    def build_schedule(self, owner: Owner) -> list[Task]:
        """Create and store a schedule spanning all of the owner's pets."""
        self.schedule = self.organize_tasks(owner)
        return self.schedule.copy()

    def complete_task(self, owner: Owner, task_id: str) -> bool:
        """Mark one task complete after finding it among all owner tasks."""
        for task in self.retrieve_tasks(owner):
            if task.task_id == task_id:
                task.mark_complete()
                return True
        return False
