"""Core models and scheduling logic for the PawPal+ pet-care planner."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from uuid import uuid4


@dataclass
class Task:
    """A single care activity assigned to a pet."""

    description: str
    time: str
    frequency: str
    completed: bool = False
    scheduled_date: date = field(default_factory=date.today)
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

    def is_recurring(self) -> bool:
        """Return ``True`` when this task repeats daily or weekly.

        One-time tasks return ``False`` and are not recreated after completion.
        """
        return self.frequency in {"daily", "weekly"}

    def create_next_occurrence(self) -> Task | None:
        """Create a new incomplete occurrence for a recurring task.

        A daily task is scheduled for tomorrow and a weekly task is scheduled
        for one week from today. One-time tasks return ``None``.
        """
        if self.frequency == "daily":
            next_date = date.today() + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = date.today() + timedelta(weeks=1)
        else:
            return None
        return Task(
            self.description,
            self.time,
            self.frequency,
            scheduled_date=next_date,
        )


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

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return a new task list ordered by its zero-padded ``HH:MM`` time.

        Args:
            tasks: The tasks to order; the original list is not modified.

        Returns:
            A chronologically ordered list of the supplied tasks.
        """
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self,
        owner: Owner,
        *,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return owner tasks matching optional completion and pet filters.

        Args:
            owner: The owner whose pet tasks should be searched.
            completed: ``True`` for complete tasks, ``False`` for incomplete
                tasks, or ``None`` to include either status.
            pet_name: A case-insensitive pet name, or ``None`` for all pets.

        Returns:
            Every task that satisfies all supplied filters.
        """
        normalized_pet_name = pet_name.strip().casefold() if pet_name else None
        return [
            task
            for task in self.retrieve_tasks(owner)
            if (completed is None or task.completed is completed)
            and (
                normalized_pet_name is None
                or task.pet_name is not None
                and task.pet_name.casefold() == normalized_pet_name
            )
        ]

    def get_recurring_tasks(
        self, owner: Owner, *, frequency: str | None = None
    ) -> list[Task]:
        """Return incomplete daily and weekly tasks for an owner.

        Args:
            owner: The owner whose tasks should be searched.
            frequency: Optionally limit results to ``"daily"`` or
                ``"weekly"``; case is ignored.

        Returns:
            Incomplete recurring tasks matching the optional frequency.

        Raises:
            ValueError: If ``frequency`` is not daily or weekly.
        """
        normalized_frequency = frequency.lower().strip() if frequency else None
        if normalized_frequency is not None and normalized_frequency not in {"daily", "weekly"}:
            raise ValueError("frequency must be daily or weekly when filtering recurring tasks.")

        return [
            task
            for task in self.retrieve_tasks(owner)
            if not task.completed
            and task.is_recurring()
            and (normalized_frequency is None or task.frequency == normalized_frequency)
        ]

    def detect_conflicts(self, owner: Owner) -> list[str]:
        """Return non-blocking warnings for duplicate pet date-and-time slots.

        Incomplete tasks conflict only when they belong to the same pet and
        share both ``scheduled_date`` and ``time``. Tasks for different pets
        or on different dates do not conflict.
        """
        warnings: list[str] = []
        for pet in owner.pets:
            tasks_by_slot: dict[tuple[date, str], list[Task]] = {}
            for task in pet.tasks:
                if not task.completed:
                    tasks_by_slot.setdefault((task.scheduled_date, task.time), []).append(task)

            for (scheduled_date, task_time), tasks_at_time in tasks_by_slot.items():
                if len(tasks_at_time) > 1:
                    descriptions = ", ".join(task.description for task in tasks_at_time)
                    warnings.append(
                        f"Warning: {pet.name} has multiple tasks on {scheduled_date} "
                        f"at {task_time}: {descriptions}."
                    )
        return warnings

    def organize_tasks(self, owner: Owner) -> list[Task]:
        """Return incomplete tasks ordered by their scheduled time."""
        tasks = self.retrieve_tasks(owner)
        return self.sort_by_time(
            [task for task in tasks if not task.completed]
        )

    def build_schedule(self, owner: Owner) -> list[Task]:
        """Create and store a schedule spanning all of the owner's pets."""
        self.schedule = self.organize_tasks(owner)
        return self.schedule.copy()

    def complete_task(self, owner: Owner, task_id: str) -> bool:
        """Complete one task and add a future occurrence when it recurs.

        Daily and weekly tasks remain in the pet's history as complete and
        gain a new incomplete task. One-time tasks are only marked complete.

        Returns:
            ``True`` when a matching task belongs to the owner; otherwise
            ``False``.
        """
        for pet in owner.pets:
            for task in pet.tasks:
                if task.task_id != task_id:
                    continue
                if task.completed:
                    return True

                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return True
        return False
