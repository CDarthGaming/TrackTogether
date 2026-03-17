import streamlit as st
import sqlite3
from datetime import datetime, date

from header import show_header

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
st.set_page_config(
    page_title="Track Together",
    page_icon="👾",
    layout="wide"
)
show_header()

# ---------------------------------------------------
# Check login
# ---------------------------------------------------
user_id = st.session_state.get("user_id")
assignment_id = st.session_state.get("selected_assignment")
if not user_id or not assignment_id:
    st.error("You must be logged in and have selected an assignment!")
    st.stop()

# ---------------------------------------------------
# Connect database
# ---------------------------------------------------
conn_modules = sqlite3.connect("modules.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn_modules.cursor()
cursor.execute("ATTACH DATABASE 'users.db' AS users_db")

# ---------------------------------------------------
# Helper: progress bar color
# ---------------------------------------------------
def progress_color(percent: int) -> str:
    if percent < 40:
        return "red"
    elif percent < 75:
        return "orange"
    else:
        return "green"

# ---------------------------------------------------
# Fetch assignment info and student progress
# ---------------------------------------------------
cursor.execute("""
    SELECT a.id, a.name, a.start_date, a.due_date, a.weighting,
           m.code AS module_code, m.name AS module_name,
           sa.progress, sa.complete, sa.notes
    FROM assignments a
    JOIN modules m ON m.id = a.module_id
    JOIN student_assignments sa
        ON sa.assignment_id = a.id AND sa.student_id = ?
    WHERE a.id = ?
""", (user_id, assignment_id))

row = cursor.fetchone()
if not row:
    st.error("Assignment not found for this student!")
    st.stop()

(a_id, a_name, start_date, due_date, weighting,
 module_code, module_name, progress, complete, notes) = row

# Format dates
start_date = start_date if isinstance(start_date, date) else datetime.strptime(start_date, "%Y-%m-%d").date()
due_date = due_date if isinstance(due_date, date) else datetime.strptime(due_date, "%Y-%m-%d").date()

st.title(f"{a_name} ({weighting}%)")

# ---------------------------------------------------
# Progress bar + complete button
# ---------------------------------------------------
col1, col2 = st.columns([4,1])

# Progress bar
progress_color_hex = progress_color(progress)
col1.markdown(f"""
<div style="background-color:#ccc;border-radius:6px;height:14px;">
    <div style="
        width:{progress}%;
        background-color:{progress_color_hex};
        height:14px;
        border-radius:6px;">
    </div>
</div>
<small>{progress}% complete</small>
""", unsafe_allow_html=True)

# Complete button
today = date.today()
can_complete = progress >= 75 or today >= due_date
if not complete:
    if col2.button("Complete Assignment", disabled=not can_complete):
        cursor.execute("""
            UPDATE student_assignments
            SET complete=1, progress=100
            WHERE student_id=? AND assignment_id=?
        """, (user_id, assignment_id))
        conn_modules.commit()
        st.toast("Assignment marked complete! 🎉")
        st.rerun()
else:
    if col2.button("Uncomplete Assignment", key=f"uncomplete_{a_id}"):
        cursor.execute("""
            UPDATE student_assignments
            SET complete=0, progress=0
            WHERE student_id=? AND assignment_id=?
        """, (user_id, a_id))
        conn_modules.commit()
        st.toast("Assignment marked incomplete.")
        st.rerun()

st.divider()

# ---------------------------------------------------
# Assignment info
# ---------------------------------------------------
col1, col2 = st.columns(2)
col1.markdown(f"**Module Name:** {module_name}")
col2.markdown(f"**Start Date:** {start_date}")

col3, col4 = st.columns(2)
col3.markdown(f"**Module Code:** {module_code}")
col4.markdown(f"**Due Date:** {due_date}")

st.divider()

st.header("Enter Achieved Grade:")

conn_modules = sqlite3.connect("modules.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor_modules = conn_modules.cursor()
cursor_modules.execute("ATTACH DATABASE 'users.db' AS users_db")

cursor_modules.execute("""
    SELECT achieved_grade
    FROM student_assignments
    WHERE student_id=? AND assignment_id=?
""", (user_id, a_id))

result = cursor_modules.fetchone()

achieved_grade = result[0] if result and result[0] is not None else 0

st.caption("Grade cannot be entered until assignment complete.")

grade = st.number_input(
    label="",
    label_visibility="hidden",
    min_value=0,
    max_value=100,
    value=achieved_grade,
    disabled=not complete,
    key=f"grade_{a_id}"
)

if st.button("Save", key=f"save_grade_{a_id}"):
    if complete:
        cursor_modules.execute("""
            UPDATE student_assignments
            SET achieved_grade=?
            WHERE student_id=? AND assignment_id=?
        """, (grade, user_id, a_id))

        conn_modules.commit()
        st.toast("Grade saved!",icon="🖊️")
    else:
        st.warning("Grade cannot be entered until assignment complete.",icon="⚠️")

st.divider()

# ---------------------------------------------------
# Tasks
# ---------------------------------------------------
st.subheader("Tasks")

# ---------------------------------------------------
# Add a new task form
# ---------------------------------------------------
if not complete:
    with st.expander("Add a New Task"):
        with st.form("add_task_form"):
            task_name = st.text_input("Task Name")
            task_due = st.date_input("Due Date")
            task_desc = st.text_area("Description")
            submitted = st.form_submit_button("Add Task")

            if submitted:
                if not task_name:
                    st.warning("Task must have a name!")
                else:
                    cursor.execute("""
                        INSERT INTO tasks (assignment_id, student_id, name, description, due_date, completed)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (assignment_id, user_id, task_name, task_desc, str(task_due), 0))
                    conn_modules.commit()
                    st.toast(f"Task '{task_name}' added! 📝")
                    st.rerun()
else:
    st.warning(body="Tasks have been locked for complete assignments.",icon="⚠️")
    st.success(body="You can still add to your notes.",icon="😀")

cursor.execute("""
    SELECT id, name, description, due_date, completed
    FROM tasks
    WHERE assignment_id=?
    ORDER BY due_date
""", (assignment_id,))
tasks = cursor.fetchall()

if not tasks and not complete:
    st.info("No tasks yet.")

for t_id, t_name, t_desc, t_due, t_completed in tasks:
    # Format date
    t_due = t_due if isinstance(t_due, date) else datetime.strptime(t_due, "%Y-%m-%d").date()
    cols = st.columns([3,2,4,1])

    # Task name
    if t_completed:
        cols[0].markdown(f":gray[{t_name}]")
    else:
        cols[0].write(t_name)

    # Due date
    if not t_completed and t_due < today:
        cols[1].markdown(f":red[{t_due}]")
    else:
        cols[1].write(t_due)

    # Description
    cols[2].write(t_desc)

    # Completion checkbox
    if not complete:
        checked = cols[3].checkbox("", value=bool(t_completed), key=f"task_{t_id}")
        if checked != bool(t_completed):
            cursor.execute("""
                UPDATE tasks SET completed=? WHERE id=?
            """, (int(checked), t_id))
            # Recalculate progress
            cursor.execute("""
                SELECT COUNT(*) FROM tasks WHERE assignment_id=?
            """, (assignment_id,))
            total_tasks = cursor.fetchone()[0]
            cursor.execute("""
                SELECT COUNT(*) FROM tasks WHERE assignment_id=? AND completed=1
            """, (assignment_id,))
            completed_tasks = cursor.fetchone()[0]
            progress_percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
            cursor.execute("""
                UPDATE student_assignments SET progress=? WHERE student_id=? AND assignment_id=?
            """, (progress_percent, user_id, assignment_id))
            conn_modules.commit()
            st.rerun()
    else:
        cols[3].write("✔" if t_completed else "")

st.divider()

# ---------------------------------------------------
# Notes
# ---------------------------------------------------
st.subheader("Notes")
notes_value = st.text_area("", value=notes or "", height=200)
if st.button("Save Notes"):
    cursor.execute("""
        UPDATE student_assignments SET notes=? WHERE student_id=? AND assignment_id=?
    """, (notes_value, user_id, assignment_id))
    conn_modules.commit()
    st.toast("Notes saved! 📜")

st.divider()

# ---------------------------------------------------
# Return
# ---------------------------------------------------
if st.button("Return to Assignments"):
    st.switch_page("pages/view_assignments.py")