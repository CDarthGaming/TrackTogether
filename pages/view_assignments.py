import streamlit as st
import sqlite3
import time
from datetime import datetime, date

from header import show_header

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
st.set_page_config(page_title="Track Together", page_icon="👾", layout="wide")
show_header()

# ---------------------------------------------------
# Check login
# ---------------------------------------------------
user_id = st.session_state.get("user_id")
if not user_id:
    st.error("You must be logged in!")
    st.stop()

# ---------------------------------------------------
# Connect databases
# ---------------------------------------------------
conn_modules = sqlite3.connect("modules.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor_modules = conn_modules.cursor()
cursor_modules.execute("ATTACH DATABASE 'users.db' AS users_db")

# ---------------------------------------------------
# Reminder to enter grades for completed assignments
# ---------------------------------------------------
cursor_modules.execute("""
    SELECT a.name
    FROM assignments a
    JOIN student_assignments sa
        ON sa.assignment_id = a.id
    WHERE sa.student_id=? 
    AND sa.complete=1
    AND (sa.achieved_grade IS NULL OR sa.achieved_grade=0)
""", (user_id,))

missing_grades = cursor_modules.fetchall()

if missing_grades:
    count = len(missing_grades)
    st.warning(f"⚠️ {count} completed assignment(s) still need a grade entered.")

    for assignment in missing_grades:
        st.badge(f"{assignment[0]}")

# ---------------------------------------------------
# Get student info
# ---------------------------------------------------
cursor_modules.execute("SELECT course_id, year, fName, surname FROM users_db.users WHERE id=?", (user_id,))
student = cursor_modules.fetchone()
if not student:
    st.error("Student not found!")
    st.stop()

course_id, year, fName, surname = student
st.title(f"Assignments for {fName} {surname}")

# ---------------------------------------------------
# Fetch modules for student
# ---------------------------------------------------
cursor_modules.execute("""
    SELECT m.id, m.code, m.name
    FROM modules m
    JOIN course_modules cm ON cm.module_id = m.id
    WHERE cm.course_id=? AND cm.year=?
    ORDER BY m.code
""", (course_id, year))
modules = cursor_modules.fetchall()
if not modules:
    st.info("No modules found for your course/year.")
    st.stop()

# --- populate student_assignments for this student ---
for m_id, m_code, m_name in modules:
    cursor_modules.execute("""
        SELECT id FROM assignments WHERE module_id=?
    """, (m_id,))
    assignment_ids = [row[0] for row in cursor_modules.fetchall()]

    for a_id in assignment_ids:
        cursor_modules.execute("""
            INSERT OR IGNORE INTO student_assignments (student_id, assignment_id, progress, complete)
            VALUES (?, ?, 0, 0)
        """, (user_id, a_id))
conn_modules.commit()

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
# Display assignments per module
# ---------------------------------------------------
for m_id, m_code, m_name in modules:
    st.subheader(f"{m_code} - {m_name}")

    cursor_modules.execute("""
        SELECT a.id, a.name, a.start_date, a.due_date, a.weighting,
            sa.progress, sa.complete
        FROM assignments a
        JOIN student_assignments sa
            ON sa.assignment_id = a.id AND sa.student_id = ?
        WHERE a.module_id=?
        ORDER BY a.id
    """, (user_id, m_id))

    assignments = cursor_modules.fetchall()

    if not assignments:
        st.info("No assignments found for this module.")
        continue

    for a_id, a_name, start_date, due_date, weighting, progress, complete in assignments:
        # Format dates
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if isinstance(start_date, str) else start_date
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if isinstance(due_date, str) else due_date

        # Columns for a clean layout
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([3, 1, 1, 1, 0.5, 0.75, 1, 1, 1])

        # Assignment name + weighting
        # conn_modules = sqlite3.connect("modules.db", detect_types=sqlite3.PARSE_DECLTYPES)
        # cursor_modules = conn_modules.cursor()
        # cursor_modules.execute("ATTACH DATABASE 'users.db' AS users_db")

        # result = cursor_modules.execute("""
        #     SELECT achieved_grade
        #     FROM student_assignments
        #     WHERE student_id=? AND assignment_id=?
        # """, (user_id, a_id))

        # if complete and (result is None or result == 0):
        #     col1.markdown(f":red[**{a_name}**]")
        # else:
        #     col1.markdown(f"**{a_name}**")
        
        col1.markdown(f"**{a_name}** ({weighting}%)")

        # Start and due dates
        col2.markdown(f"Start: {start_date}")
        col3.markdown(f"Due: {due_date}")

        # Progress bar
        progress_color_hex = progress_color(progress)
        col4.markdown(
            f"""
            <div style="background-color:#ccc;border-radius:5px;height:12px;">
                <div style="
                    width:{progress}%;
                    background-color:{progress_color_hex};
                    height:12px;
                    border-radius:5px;">
                </div>
            </div>
            <small>{progress}%</small>
            """,
            unsafe_allow_html=True
        )

        # View button
        if col8.button("View", key=f"view_{a_id}"):
            st.session_state["selected_assignment"] = a_id
            st.switch_page("pages/view_details.py")

        # Complete / Uncomplete button
        today = date.today()
        can_complete = progress >= 75 or today >= due_date

        if not complete:
            if col9.button("Complete", key=f"complete_{a_id}", disabled=not can_complete):
                cursor_modules.execute("""
                    UPDATE student_assignments
                    SET complete=1, progress=100
                    WHERE student_id=? AND assignment_id=?
                """, (user_id, a_id))
                conn_modules.commit()
                st.toast("Assignment marked complete, congrats! 🎉")
                st.balloons()
                time.sleep(1)
                st.toast("Once you've recieved your grade from your lecturer, click 'view' and add your grade to the system!",icon="😀")
                time.sleep(5)
                st.rerun()
        else:
            if col9.button("Uncomplete", key=f"uncomplete_{a_id}"):
                cursor_modules.execute("""
                    UPDATE student_assignments
                    SET complete=0, progress=0
                    WHERE student_id=? AND assignment_id=?
                """, (user_id, a_id))
                conn_modules.commit()
                st.toast("Assignment marked incomplete.")
                time.sleep(1)
                st.rerun()

