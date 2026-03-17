import streamlit as st
import sqlite3
import pandas as pd
import time
from header import show_header

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Admin Panel",
    page_icon="👾",
    layout="wide"
)

show_header()
st.title("Admin: Manage Courses, Modules & Users")

# ---------------------------------------------------
# Session check & verify admin
# ---------------------------------------------------
if "user_id" not in st.session_state:
    st.error("You must be logged in as an admin to access this page.")
    st.stop()

user_id = st.session_state["user_id"]

conn_users = sqlite3.connect("users.db")
cursor_users = conn_users.cursor()
cursor_users.execute("SELECT admin FROM users WHERE id=?", (user_id,))
result = cursor_users.fetchone()
if not result or not result[0]:
    st.error("You do not have admin permissions!")
    st.stop()

# ---------------------------------------------------
# Modules DB connection
# ---------------------------------------------------
conn_modules = sqlite3.connect("modules.db")
cursor_modules = conn_modules.cursor()

# -------------------------
# Section 1: Add a new course
# -------------------------
st.subheader("Add a New Course")
with st.form("add_course_form"):
    new_course = st.text_input("Course Name")
    submitted_course = st.form_submit_button("Add Course")
    if submitted_course:
        if not new_course.strip():
            st.warning("Course name cannot be blank.")
        else:
            cursor_modules.execute("INSERT OR IGNORE INTO courses (name) VALUES (?)", (new_course.strip(),))
            conn_modules.commit()
            st.success(f"Course '{new_course}' added successfully!")

# -------------------------
# Section 2: Add a new module
# -------------------------
st.subheader("Add a New Module")
with st.form("add_module_form"):
    module_code = st.text_input("Module Code (e.g., CS101)", max_chars=6)
    module_name = st.text_input("Module Name")
    submitted_module = st.form_submit_button("Add Module")
    if submitted_module:
        if not module_code or not module_name:
            st.warning("Module code and name cannot be blank.")
        else:
            cursor_modules.execute(
                "INSERT OR IGNORE INTO modules (code, name) VALUES (?, ?)",
                (module_code.strip(), module_name.strip())
            )
            conn_modules.commit()
            st.success(f"Module '{module_code} - {module_name}' added successfully!")

# -------------------------
# Section 3: Associate modules with course/year
# -------------------------
st.subheader("Associate Modules with Courses & Years")
with st.form("associate_module_form"):
    cursor_modules.execute("SELECT id, name FROM courses")
    courses = cursor_modules.fetchall()
    cursor_modules.execute("SELECT id, code, name FROM modules")
    modules = cursor_modules.fetchall()

    if not courses or not modules:
        st.info("Add some courses and modules first!")
    else:
        course_dict = {name: cid for cid, name in courses}
        module_dict = {f"{code} - {name}": mid for mid, code, name in modules}

        selected_course = st.selectbox("Select Course", list(course_dict.keys()))
        selected_module = st.selectbox("Select Module", list(module_dict.keys()))
        selected_year = st.selectbox("Select Year", [0, 1, 2, 3, 4])

    submitted_assoc = st.form_submit_button("Associate Module")
    if submitted_assoc:
        course_id = course_dict[selected_course]
        module_id = module_dict[selected_module]

        cursor_modules.execute(
            "INSERT OR IGNORE INTO course_modules (course_id, module_id, year) VALUES (?, ?, ?)",
            (course_id, module_id, selected_year)
        )
        conn_modules.commit()
        st.success(f"Module '{selected_module}' associated with '{selected_course}' year {selected_year}!")

# -------------------------
# Section 4: Modify Course
# -------------------------
st.subheader("Modify Course")
with st.form("modify_course_form"):
    if courses:
        course_dict = {name: cid for cid, name in courses}
        selected_course_label = st.selectbox("Select a course to modify", list(course_dict.keys()))
        new_course_name = st.text_input("New course name")
        submitted_modify_course = st.form_submit_button("Update Course Name")
        if submitted_modify_course:
            if new_course_name.strip():
                cursor_modules.execute("UPDATE courses SET name=? WHERE id=?", (new_course_name.strip(), course_dict[selected_course_label]))
                conn_modules.commit()
                st.success("Course name updated!")
                time.sleep(0.25)
                st.rerun()
            else:
                st.warning("Enter a new name!")

# -------------------------
# Section 5: Modify Module
# -------------------------
st.subheader("Modify Module")
with st.form("modify_module_form"):
    if modules:
        module_dict = {f"{m_code} - {m_name} (ID: {m_id})": m_id for m_id, m_code, m_name in modules}
        selected_module_label = st.selectbox("Select a module to modify", list(module_dict.keys()))
        new_module_name = st.text_input("New module name")
        new_module_code = st.text_input("New module code")
        submitted_modify_module = st.form_submit_button("Update Module")
        if submitted_modify_module:
            module_id = module_dict[selected_module_label]
            if new_module_name.strip():
                cursor_modules.execute("UPDATE modules SET name=? WHERE id=?", (new_module_name.strip(), module_id))
            if new_module_code.strip():
                cursor_modules.execute("UPDATE modules SET code=? WHERE id=?", (new_module_code.strip(), module_id))
            conn_modules.commit()
            st.success("Module updated!")
            time.sleep(0.25)
            st.rerun()

# -------------------------
# Section 6: Modify Associations
# -------------------------
st.subheader("Modify Course-Module Associations")
with st.form("modify_assoc_form"):
    if courses and modules:
        course_dict = {name: cid for cid, name in courses}
        module_dict = {f"{m_code} - {m_name} (ID: {m_id})": m_id for m_id, m_code, m_name in modules}

        selected_course_label = st.selectbox("Select course to update associations", list(course_dict.keys()))
        selected_year = st.selectbox("Select year for this course", [0, 1, 2, 3, 4])

        course_id = course_dict[selected_course_label]
        cursor_modules.execute("SELECT module_id FROM course_modules WHERE course_id=? AND year=?", (course_id, selected_year))
        current_assoc = [row[0] for row in cursor_modules.fetchall()]

        selected_modules = st.multiselect(
            "Select modules for this course/year",
            options=list(module_dict.keys()),
            default=[k for k, v in module_dict.items() if v in current_assoc]
        )

        submitted_modify_assoc = st.form_submit_button("Update Associations")
        if submitted_modify_assoc:
            cursor_modules.execute("DELETE FROM course_modules WHERE course_id=? AND year=?", (course_id, selected_year))
            for m_label in selected_modules:
                cursor_modules.execute(
                    "INSERT INTO course_modules (course_id, module_id, year) VALUES (?, ?, ?)",
                    (course_id, module_dict[m_label], selected_year)
                )
            conn_modules.commit()
            st.success("Course-module associations updated!")
            time.sleep(0.25)
            st.rerun()

# -------------------------
# Section 7: User Management (Improved Layout)
# -------------------------
st.subheader("Manage Users")

# -------------------------
# Fetch students
# -------------------------
cursor_users.execute(
    "SELECT id, username, fName, surname, admin, course_id, year FROM users WHERE role='Student'"
)
students = cursor_users.fetchall()
if students:
    student_df = pd.DataFrame(students, columns=["id", "Username", "First Name", "Surname", "Admin", "CourseID", "Year"])
    student_df["Admin"] = student_df["Admin"].astype(bool)

    st.write("### Students")
    edited_students = st.data_editor(
        student_df,
        column_config={
            "Admin": st.column_config.CheckboxColumn("Admin?", help="Toggle admin permission")
        },
        hide_index=True,
        key="students_editor"
    )
else:
    st.info("No students found.")
    edited_students = pd.DataFrame()

# -------------------------
# Fetch lecturers
# -------------------------
cursor_users.execute(
    "SELECT id, username, fName, surname, admin, approved FROM users WHERE role='Lecturer'"
)
lecturers = cursor_users.fetchall()
if lecturers:
    lecturer_df = pd.DataFrame(lecturers, columns=["id", "Username", "First Name", "Surname", "Admin", "Approved"])
    lecturer_df["Admin"] = lecturer_df["Admin"].astype(bool)
    lecturer_df["Approved"] = lecturer_df["Approved"].astype(bool)

    st.write("### Lecturers")
    edited_lecturers = st.data_editor(
        lecturer_df,
        column_config={
            "Admin": st.column_config.CheckboxColumn("Admin?", help="Toggle admin permission"),
            "Approved": st.column_config.CheckboxColumn("Approve?", help="Toggle lecturer approval")
        },
        hide_index=True,
        key="lecturers_editor"
    )
else:
    st.info("No lecturers found.")
    edited_lecturers = pd.DataFrame()

# -------------------------
# Submit Button
# -------------------------
if st.button("Update Users"):
    # Update students
    for _, row in edited_students.iterrows():
        cursor_users.execute(
            "UPDATE users SET admin=? WHERE id=?",
            (int(row["Admin"]), row["id"])
        )

    # Update lecturers
    for _, row in edited_lecturers.iterrows():
        cursor_users.execute(
            "UPDATE users SET admin=?, approved=? WHERE id=?",
            (int(row["Admin"]), int(row["Approved"]), row["id"])
        )

    conn_users.commit()
    st.success("User permissions and approvals updated!")

# -------------------------
# Section 8: View Course - Module Associations
# -------------------------
st.subheader("View Course - Module Associations")
cursor_modules.execute("SELECT id, name FROM courses ORDER BY name")
courses = cursor_modules.fetchall()
if courses:
    course_dict = {name: cid for cid, name in courses}
    selected_course = st.selectbox("Select Course", list(course_dict.keys()))

    cursor_modules.execute("SELECT DISTINCT year FROM course_modules WHERE course_id=?", (course_dict[selected_course],))
    years = [row[0] for row in cursor_modules.fetchall()]
    if years:
        selected_year = st.selectbox("Select Year", years)

        cursor_modules.execute("""
            SELECT m.code, m.name
            FROM course_modules cm
            JOIN modules m ON cm.module_id = m.id
            WHERE cm.course_id=? AND cm.year=?
            ORDER BY m.code
        """, (course_dict[selected_course], selected_year))
        modules = cursor_modules.fetchall()

        if modules:
            st.write(f"Modules for {selected_course} - Year {selected_year}:")
            for code, name in modules:
                st.write(f"{code} {name}")
        else:
            st.info("No modules associated for this course/year.")
    else:
        st.info("No years found for this course.")
else:
    st.info("No courses available. Add courses first!")

# ---------------------------------------------------
# Close connections
# ---------------------------------------------------
conn_modules.close()
conn_users.close()