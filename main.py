"""Temporary command-line demo for the PawPal+ scheduling system."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Create sample pets/tasks and print one owner-wide daily schedule."""
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "cat", age=3)
    biscuit = Pet("Biscuit", "dog", age=5)

    mochi.add_task(Task("Breakfast", "08:00", "daily"))
    mochi.add_task(Task("Playtime", "17:30", "daily"))
    biscuit.add_task(Task("Morning walk", "07:30", "daily"))
    biscuit.add_task(Task("Medication", "20:00", "daily"))

    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    scheduler = Scheduler()
    schedule = scheduler.build_schedule(owner)

    print("Today's Schedule")
    print("=" * 18)
    for task in schedule:
        print(
            f"{task.time} — {task.pet_name}: {task.description} "
            f"({task.frequency})"
        )


if __name__ == "__main__":
    main()
