import streamlit as st

if "tasks" not in st.session_state:
    st.session_state.tasks = []

def main_page():
    st.title("Start a New Session")
    if st.button("Start"):
        st.session_state.page = "tasks"

# callback to clear input
def clear_task_input():
    st.session_state.task_input = ""

def tasks_page():
    st.title("Tasks to Complete")
    new_task = st.text_input("Enter a new task:", key="task_input")

    if st.button("+ Add Task", on_click=clear_task_input):
        if new_task.strip():
            st.session_state.tasks.append(new_task.strip())

    st.write("---")

    delete_indices = []
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([6, 1])
        cols[0].write(task)
        if cols[1].button("X", key=f"delete_{i}"):
            delete_indices.append(i)

    for i in sorted(delete_indices, reverse=True):
        st.session_state.tasks.pop(i)

if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "tasks":
    tasks_page()
