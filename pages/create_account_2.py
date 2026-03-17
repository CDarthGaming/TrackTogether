import streamlit as st
import sqlite3
import bcrypt
import time

st.set_page_config(
    page_title="Track Together",
    page_icon="👾",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #FDFDFC;
        text-color: #0f0f0f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Select Your Course and Year")

if "new_user" not in st.session_state:
    st.error("No registration data found! Please start from the first page.")
    st.stop()

new_user = st.session_state['new_user']

# Connect to modules DB to get courses
conn_modules = sqlite3.connect("modules.db")
cursor_modules = conn_modules.cursor()

cursor_modules.execute("SELECT id, name FROM courses")
courses = cursor_modules.fetchall()
course_dict = {name: cid for cid, name in courses}

if not courses:
    st.error("No courses found! Contact an admin to add courses.")
    st.stop()

selected_course = st.selectbox("Select Course", list(course_dict.keys()))
selected_year = st.selectbox("Select Year", [0, 1, 2, 3, 4])

if st.button("Create Account"):
    hashed = bcrypt.hashpw(new_user['password'].encode(), bcrypt.gensalt()).decode()

    conn_users = sqlite3.connect("users.db")
    cursor_users = conn_users.cursor()

    cursor_users.execute(
        """
        INSERT INTO users (username, password, fName, surname, email, role, course_id, year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            new_user['username'],
            hashed,
            new_user['fname'],
            new_user['surname'],
            new_user['email'],
            "Student",
            course_dict[selected_course],
            selected_year
        )
    )
    conn_users.commit()
    conn_users.close()

    st.success("Student account created successfully!")
    del st.session_state['new_user']
    time.sleep(1)
    st.switch_page("streamlit_app.py")

# ---------------------------------------------------
# Return button
# ---------------------------------------------------
if st.button("Return to Login page"):
    st.switch_page("streamlit_app.py")