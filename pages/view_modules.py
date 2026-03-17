import streamlit as st
import sqlite3
import time
from datetime import datetime, timedelta

from header import show_header

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Track Together",
    page_icon="👾",
    layout="wide"
)

show_header()

# ---------------------------------------------------
# Styling
# ---------------------------------------------------
st.markdown("""
<style>
img {
    border-radius:50%;
    object-fit:cover;
}
.profile-header {
    display:flex;
    align-items:center;
    gap:20px;
}
</style>
""", unsafe_allow_html=True)

st.title("Lecturer: Manage Your Modules & Assignments")

if "user_id" not in st.session_state:
    st.error("You must be logged in to access this page.")
    st.stop()

lecturer_id = st.session_state["user_id"]

# ---------------------------------------------------
# Connect to DBs
# ---------------------------------------------------
conn_modules = sqlite3.connect("modules.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor_modules = conn_modules.cursor()

conn_users = sqlite3.connect("users.db")
cursor_users = conn_users.cursor()

# ---------------------------------------------------
# Fetch all modules
# ---------------------------------------------------
cursor_modules.execute("SELECT id, code, name FROM modules ORDER BY code")
all_modules = cursor_modules.fetchall()
module_dict = {f"{code} - {name}": mid for mid, code, name in all_modules}

# ---------------------------------------------------
# Section 1: Select modules they teach
# ---------------------------------------------------
st.subheader("Select Modules You Teach")
cursor_modules.execute(
    "SELECT module_id FROM lecturer_modules WHERE lecturer_id=?",
    (lecturer_id,)
)
current_module_ids = [row[0] for row in cursor_modules.fetchall()]

with st.form("select_modules_form"):
    selected_modules = st.multiselect(
        "Select Modules:",
        options=list(module_dict.keys()),
        default=[k for k, v in module_dict.items() if v in current_module_ids]
    )
    submitted_modules = st.form_submit_button("Save Module Selection")
    if submitted_modules:
        # Clear old selections
        cursor_modules.execute("DELETE FROM lecturer_modules WHERE lecturer_id=?", (lecturer_id,))
        conn_modules.commit()

        for m_label in selected_modules:
            module_id = module_dict[m_label]
            cursor_modules.execute(
                "INSERT OR IGNORE INTO lecturer_modules (lecturer_id, module_id) VALUES (?, ?)",
                (lecturer_id, module_id)
            )

            # --- AUTOMATIC ASSIGNMENT CREATION ---
            cursor_modules.execute("SELECT COUNT(*) FROM assignments WHERE module_id=?", (module_id,))
            current_count = cursor_modules.fetchone()[0]
            # Create assignments until there are 2
            for i in range(current_count + 1, 3):
                default_name = f"Assignment {i}"
                start_date = datetime.today().date()
                due_date = (datetime.today() + timedelta(days=14)).date()
                weighting = 50
                cursor_modules.execute(
                    "INSERT INTO assignments (module_id, name, start_date, due_date, weighting) VALUES (?, ?, ?, ?, ?)",
                    (module_id, default_name, start_date, due_date, weighting)
                )

        conn_modules.commit()
        st.success("Module selections saved! Default assignments created where needed.")
        time.sleep(0.5)
        st.rerun()

# -------------------------
# Section 2: List modules they teach and allow assignment edits
# -------------------------
st.subheader("Your Modules & Assignments")

# Fetch modules again in case of update
cursor_modules.execute(
    "SELECT m.id, m.code, m.name FROM modules m "
    "JOIN lecturer_modules lm ON lm.module_id = m.id "
    "WHERE lm.lecturer_id=? ORDER BY m.code",
    (lecturer_id,)
)
lecturer_modules = cursor_modules.fetchall()

if not lecturer_modules:
    st.info("You are not assigned to any modules yet.")
else:
    for m_id, m_code, m_name in lecturer_modules:
        st.markdown(f"### {m_code} - {m_name}")
        
        # Fetch 2 assignments per module, now including weighting
        cursor_modules.execute(
            "SELECT id, name, start_date, due_date, weighting FROM assignments WHERE module_id=? ORDER BY id LIMIT 2",
            (m_id,)
        )
        assignments = cursor_modules.fetchall()

        # Auto-create assignments if missing
        while len(assignments) < 2:
            new_id = len(assignments) + 1
            default_name = f"Assignment {new_id}"
            start_date = datetime.today().date()
            due_date = (datetime.today() + timedelta(days=14)).date()
            default_weighting = 50
            cursor_modules.execute(
                "INSERT INTO assignments (module_id, name, start_date, due_date, weighting) VALUES (?, ?, ?, ?, ?)",
                (m_id, default_name, start_date, due_date, default_weighting)
            )
            conn_modules.commit()
            last_id = cursor_modules.lastrowid
            assignments.append((last_id, default_name, start_date, due_date, default_weighting))

        # Display editable forms for each assignment
        for a_id, a_name, start_date, due_date, weighting in assignments:
            with st.form(f"assignment_form_{a_id}"):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    new_name = st.text_input("Assignment Name", value=a_name)
                with col2:
                    new_start = st.date_input("Start Date", value=datetime.strptime(str(start_date), "%Y-%m-%d").date())
                with col3:
                    new_due = st.date_input("Due Date", value=datetime.strptime(str(due_date), "%Y-%m-%d").date())
                with col4:
                    new_weight = st.number_input("Weighting (%)", min_value=0, max_value=100, value=weighting)
                
                submitted_assign = st.form_submit_button("Update Assignment")
                if submitted_assign:
                    cursor_modules.execute(
                        "UPDATE assignments SET name=?, start_date=?, due_date=?, weighting=? WHERE id=?",
                        (new_name, new_start, new_due, new_weight, a_id)
                    )
                    conn_modules.commit()
                    st.success("Assignment updated!")
                    time.sleep(0.5)
                    st.rerun()

conn_modules.close()
conn_users.close()