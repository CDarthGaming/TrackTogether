import streamlit as st
import sqlite3
import bcrypt
import time

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
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

st.title("Welcome to Track Together")
st.write("Please create an account below")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# --------------------------------
# Form: basic info + role selection
# --------------------------------
with st.form("register_form"):
    username = st.text_input("Username", placeholder="Username here...")
    password = st.text_input("Password", type="password", placeholder="Password here...")
    fName = st.text_input("First Name", placeholder="First name here...")
    sName = st.text_input("Surname", placeholder="Surname here...")
    uniEmail = st.text_input("Email", placeholder="University email here...")
    
    role = st.radio("Account type:", ["Student", "Lecturer"])

    submitted = st.form_submit_button("Next")

    if submitted:
        if not all([username, password, fName, sName, uniEmail]):
            st.warning("Please fill in all fields.")
        elif not uniEmail.endswith("@lancashire.ac.uk"):
            st.warning("You must use a University of Lancashire email.")
        else:
            # Check username/email uniqueness
            cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                st.warning("Username already exists.")
            else:
                cursor.execute("SELECT 1 FROM users WHERE email=?", (uniEmail,))
                if cursor.fetchone():
                    st.warning("Email already registered.")
                else:
                    # Store form data in session_state
                    st.session_state['new_user'] = {
                        "username": username,
                        "password": password,
                        "fname": fName,
                        "surname": sName,
                        "email": uniEmail,
                        "role": role
                    }

                    if role == "Lecturer":
                        # Hash password and insert immediately (pending approval)
                        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                        cursor.execute(
                            """
                            INSERT INTO users (username, password, fName, surname, email, role, approved)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (username, hashed, fName, sName, uniEmail, "Lecturer", 0)
                        )
                        conn.commit()
                        st.success("Lecturer account created! Awaiting admin approval.")
                        time.sleep(1)
                        st.switch_page("streamlit_app.py")
                    else:
                        # Student continues to next page
                        st.success("Student info saved! Continue to select course and year.")
                        time.sleep(1)
                        st.switch_page("pages/create_account_2.py")

conn.close()

# ---------------------------------------------------
# Return button
# ---------------------------------------------------
if st.button("Return to Login page"):
    st.switch_page("streamlit_app.py")