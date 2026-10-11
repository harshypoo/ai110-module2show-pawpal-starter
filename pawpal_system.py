"""Class skeletons for the PawPal+ pet-care planner.

These dataclasses define the system design only.  Scheduling behavior will be
implemented in a later step.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from uuid import uuid4


@dataclass
class CareTask:
    """One pet-care activity, such as feeding, walking, or medication."""

    title: str
    duration_minutes: int
    priority: str
    category: str = "general"
    recurring: bool = False
    preferred_time: str | None = None
    task_id: str = field(default_factory=lambda: str(uuid4()))

    def is_high_priority(self) -> bool:
        """Return whether this task is marked high priority."""
        pass

    def fits_within(self, minutes: int) -> bool:
        """Return whether this task can fit in a time limit."""
        pass

    def get_priority_score(self) -> int:
        """Return a numeric score used for sorting tasks."""
        pass


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    age: int = 0
    care_tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Associate a care task with this pet."""
        pass

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by its unique ID."""
        pass

    def get_tasks(self) -> list[CareTask]:
        """Return this pet's care tasks."""
        pass


@dataclass
class PetOwner:
    """A person who owns pets and has time/preferences for their care."""

    name: str
    available_minutes: int = 0
    preferences: dict[str, object] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care."""
        pass

    def update_preference(self, setting: str, value: object) -> None:
        """Save one scheduling preference."""
        pass

    def get_available_time(self) -> int:
        """Return the time the owner has available today."""
        pass


@dataclass
class Scheduler:
    """Builds one daily plan for all of an owner's pets."""

    start_time: time = field(default_factory=lambda: time(hour=8))
    schedule: list[dict[str, object]] = field(default_factory=list, init=False)
    skipped_tasks: list[CareTask] = field(default_factory=list, init=False)

    def sort_tasks(
        self, tasks: list[CareTask], prioritize_short_tasks: bool = False
    ) -> list[CareTask]:
        """Order tasks according to priority and owner preferences."""
        pass

    def filter_tasks_by_time(
        self, tasks: list[CareTask], available_minutes: int
    ) -> list[CareTask]:
        """Keep tasks that fit within the available daily time."""
        pass

    def build_daily_plan(self, owner: PetOwner) -> list[dict[str, object]]:
        """Create one plan across every pet owned by the given owner."""
        pass

    def explain_plan(self) -> list[str]:
        """Explain why tasks were scheduled or skipped."""
        pass
