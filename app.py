"""Streamlit interface for creating and scheduling PawPal+ care tasks."""

from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def owner_key(name: str) -> str:
    """Return a stable session-state key for an owner name."""
    return name.strip().casefold()


def find_pet(owner: Owner, name: str, species: str) -> Pet | None:
    """Find an existing pet belonging to an owner by name and species."""
    for pet in owner.pets:
        if pet.name.casefold() == name.strip().casefold() and pet.species == species:
            return pet
    return None


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# These objects remain in memory for the current Streamlit browser session.
if "owners" not in st.session_state:
    st.session_state.owners: dict[str, Owner] = {}
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "active_owner_key" not in st.session_state:
    st.session_state.active_owner_key = None

st.title("🐾 PawPal+")
st.caption("Create owners, pets, and care tasks that persist during this session.")

st.subheader("1. Create or select an owner")
with st.form("owner_form", clear_on_submit=True):
    entered_owner_name = st.text_input("Owner name", placeholder="e.g., Jordan")
    create_owner = st.form_submit_button("Create or select owner")

if create_owner:
    key = owner_key(entered_owner_name)
    if not key:
        st.warning("Enter an owner name first.")
    else:
        if key not in st.session_state.owners:
            st.session_state.owners[key] = Owner(entered_owner_name.strip())
        st.session_state.active_owner_key = key

if not st.session_state.owners:
    st.info("Create an owner to begin adding pets and tasks.")
    st.stop()

owner_keys = list(st.session_state.owners)
active_key = st.session_state.active_owner_key
active_index = owner_keys.index(active_key) if active_key in owner_keys else 0
selected_owner_key = st.selectbox(
    "Active owner",
    owner_keys,
    index=active_index,
    format_func=lambda key: st.session_state.owners[key].name,
)
st.session_state.active_owner_key = selected_owner_key
active_owner = st.session_state.owners[selected_owner_key]

st.divider()
st.subheader(f"2. Add pets for {active_owner.name}")
with st.form("pet_form", clear_on_submit=True):
    entered_pet_name = st.text_input("Pet name", placeholder="e.g., Mochi")
    entered_species = st.selectbox("Species", ["dog", "cat", "other"])
    entered_age = st.number_input("Age", min_value=0, max_value=100, value=0)
    create_pet = st.form_submit_button("Create or select pet")

if create_pet:
    if not entered_pet_name.strip():
        st.warning("Enter a pet name first.")
    else:
        pet = find_pet(active_owner, entered_pet_name, entered_species)
        if pet is None:
            pet = Pet(entered_pet_name.strip(), entered_species, int(entered_age))
            active_owner.add_pet(pet)
        st.success(f"{pet.name} is ready for care tasks.")

if not active_owner.pets:
    st.info("Add a pet before creating a task.")
    st.stop()

st.divider()
st.subheader("3. Add a care task")
pet_options = {
    f"{index + 1}. {pet.name} ({pet.species})": pet
    for index, pet in enumerate(active_owner.pets)
}
with st.form("task_form", clear_on_submit=True):
    selected_pet_label = st.selectbox("Pet", list(pet_options))
    task_description = st.text_input("Task description", placeholder="e.g., Morning walk")
    task_time = st.time_input("Task time", value=time(hour=8))
    task_date = st.date_input("Scheduled date", value=date.today())
    task_frequency = st.selectbox("Frequency", ["daily", "weekly", "one-time"])
    create_task = st.form_submit_button("Add task")

if create_task:
    if not task_description.strip():
        st.warning("Enter a task description first.")
    else:
        task = Task(
            task_description,
            task_time.strftime("%H:%M"),
            task_frequency,
            scheduled_date=task_date,
        )
        pet_options[selected_pet_label].add_task(task)
        st.success(f"Added {task.description} for {task.pet_name}.")

st.divider()
st.subheader("4. View and filter tasks")
filter_pet_labels = ["All pets", *pet_options]
selected_filter_label = st.selectbox("Filter by pet", filter_pet_labels)
status_filter = st.selectbox("Filter by status", ["Incomplete", "Completed", "All"])
completed_filter = {"Incomplete": False, "Completed": True, "All": None}[status_filter]
filter_pet_name = (
    None if selected_filter_label == "All pets" else pet_options[selected_filter_label].name
)

filtered_tasks = st.session_state.scheduler.filter_tasks(
    active_owner,
    completed=completed_filter,
    pet_name=filter_pet_name,
)
filtered_tasks = st.session_state.scheduler.sort_by_time(filtered_tasks)

if filtered_tasks:
    st.table(
        [
            {
                "Date": task.scheduled_date.isoformat(),
                "Time": task.time,
                "Pet": task.pet_name,
                "Task": task.description,
                "Frequency": task.frequency,
                "Completed": task.completed,
            }
            for task in filtered_tasks
        ]
    )
else:
    st.info("No tasks match the current filters.")

recurring_tasks = st.session_state.scheduler.get_recurring_tasks(active_owner)
if recurring_tasks:
    with st.expander("Recurring tasks"):
        st.table(
            [
                {
                    "Date": task.scheduled_date.isoformat(),
                    "Time": task.time,
                    "Pet": task.pet_name,
                    "Task": task.description,
                    "Frequency": task.frequency,
                }
                for task in st.session_state.scheduler.sort_by_time(recurring_tasks)
            ]
        )

for warning in st.session_state.scheduler.detect_conflicts(active_owner):
    st.warning(warning)

with st.expander("Current pet tasks"):
    for pet in active_owner.pets:
        st.write(f"**{pet.name} ({pet.species})**")
        if pet.tasks:
            for task in st.session_state.scheduler.sort_by_time(pet.get_tasks()):
                status = "Completed" if task.completed else "Incomplete"
                st.write(
                    f"{task.scheduled_date.isoformat()} at {task.time} — "
                    f"{task.description} ({task.frequency}, {status})"
                )
                if not task.completed and st.button(
                    "Mark complete", key=f"complete_{task.task_id}"
                ):
                    st.session_state.scheduler.complete_task(active_owner, task.task_id)
                    st.rerun()
        else:
            st.caption("No tasks yet.")
