import streamlit as st
import sqlite3
import pandas as pd
import time
from header import show_header

# ---------------------------------------------------
# Page configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Track Together",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Track Together. Made by Aparna, Tabitha, Tristan."
    }
)

show_header()

# ---------------------------------------------------
# Load modules
# ---------------------------------------------------
modules_conn = sqlite3.connect("modules.db")
modules_df = pd.read_sql_query(
    """
    SELECT id, name, code
    FROM modules
    ORDER BY code
    """,
    modules_conn
)
modules_conn.close()

# ---------------------------------------------------
# Database connection for assignments
# ---------------------------------------------------
assign_conn = sqlite3.connect("assignments.db")
assign_cursor = assign_conn.cursor()

userID = st.session_state.get("user_id")

if (userID == None):
    st.switch_page("streamlit_app.py")

# ---------------------------------------------------
# Function to add new assignment
# ---------------------------------------------------
def add_assignment(name, module_name, module_code, start_date, due_date, userID):
    assign_cursor.execute(
        """
        INSERT INTO assignments (name, module_name, module_code, start_date, due_date, progress, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (name, module_name, module_code, start_date, due_date, 0, userID)
    )
    assign_conn.commit()

# ---------------------------------------------------
# Page title
# ---------------------------------------------------
st.title("Add a New Assignment")

# ---------------------------------------------------
# Assignment form
# ---------------------------------------------------
with st.form("add_assignment_form"):
    # Assignment name
    assignment_name = st.text_input("Enter Assignment Name:", max_chars=65)

    # Module selection
    module_options = {
        f"{row['code']} - {row['name']}": (row["name"], row["code"])
        for _, row in modules_df.iterrows()
    }
    selected_module = st.selectbox(
        "Select Module",
        list(module_options.keys())
    )
    module_name, module_code = module_options[selected_module]

    # Dates
    start_date = st.date_input("Start Date", value=pd.to_datetime("today"))
    due_date = st.date_input("Due Date", value=pd.to_datetime("today"))

    # Submit button
    submitted = st.form_submit_button("Add Assignment")
    if submitted:
        add_assignment(assignment_name, module_name, module_code, start_date, due_date, userID)
        st.toast("Assignment successfully added! Good luck!", icon="✏️")
        time.sleep(1)
        st.rerun()