"""Core class skeletons for the PawPal+ pet-care planner.

The classes in this file mirror the first UML draft.  Their methods are
intentionally placeholders; scheduling behavior will be added in a later step.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PetOwner:
    """A person who owns pets and has time/preferences for their care."""

    name: str
    available_minutes: int = 0
    preferences: dict[str, str] = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care."""
        pass

    def update_preference(self, setting: str, value: str) -> None:
        """Save one scheduling preference."""
        pass

    def get_available_time(self) -> int:
        """Return the time the owner has available today."""
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

    def remove_task(self, task_title: str) -> bool:
        """Remove a task by title and report whether it was found."""
        pass

    def get_tasks(self) -> list[CareTask]:
        """Return this pet's care tasks."""
        pass


@dataclass
class CareTask:
    """One pet-care activity, such as feeding, walking, or medication."""

    title: str
    duration_minutes: int
    priority: str
    category: str = "general"
    recurring: bool = False
    preferred_time: str | None = None

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
class Scheduler:
    """Builds and explains a daily pet-care plan."""

    schedule: list[dict[str, object]] = field(default_factory=list)
    skipped_tasks: list[CareTask] = field(default_factory=list)

    def sort_tasks(self, tasks: list[CareTask]) -> list[CareTask]:
        """Order tasks according to scheduling rules."""
        pass

    def filter_tasks_by_time(
        self, tasks: list[CareTask], available_minutes: int
    ) -> list[CareTask]:
        """Keep only tasks that fit within the available time."""
        pass

    def build_daily_plan(self, owner: PetOwner, pet: Pet) -> list[dict[str, object]]:
        """Create a plan for one pet using the owner's constraints."""
        pass

    def explain_plan(self) -> list[str]:
        """Explain why tasks were scheduled or skipped."""
        pass

