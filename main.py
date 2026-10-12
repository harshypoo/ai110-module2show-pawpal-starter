"""Temporary command-line demo for the PawPal+ scheduling system."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(tasks: list[Task]) -> None:
    """Print tasks in the order supplied by a scheduler method."""
    for task in tasks:
        status = "complete" if task.completed else "incomplete"
        print(f"{task.time} — {task.pet_name}: {task.description} ({status})")


def main() -> None:
    """Demonstrate sorting and filtering tasks in the terminal."""
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "cat", age=3)
    biscuit = Pet("Biscuit", "dog", age=5)

    # These are intentionally added out of chronological order.
    completed_playtime = Task("Playtime", "17:30", "daily")
    completed_playtime.mark_complete()
    mochi.add_task(completed_playtime)
    mochi.add_task(Task("Breakfast", "08:00", "daily"))
    mochi.add_task(Task("Give medication", "08:00", "daily"))
    biscuit.add_task(Task("Medication", "20:00", "daily"))
    biscuit.add_task(Task("Morning walk", "07:30", "daily"))

    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    scheduler = Scheduler()
    all_tasks = scheduler.retrieve_tasks(owner)

    print("Tasks as entered")
    print("=" * 16)
    print_tasks(all_tasks)

    print("\nSorted by time")
    print("=" * 14)
    print_tasks(scheduler.sort_by_time(all_tasks))

    print("\nBiscuit's tasks")
    print("=" * 15)
    print_tasks(scheduler.filter_tasks(owner, pet_name="Biscuit"))

    print("\nCompleted tasks")
    print("=" * 15)
    print_tasks(scheduler.filter_tasks(owner, completed=True))

    print("\nToday's incomplete schedule")
    print("=" * 27)
    print_tasks(scheduler.build_schedule(owner))

    print("\nSchedule warnings")
    print("=" * 17)
    for warning in scheduler.detect_conflicts(owner):
        print(warning)


if __name__ == "__main__":
    main()
