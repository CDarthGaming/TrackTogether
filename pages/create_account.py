import streamlit as st
import sqlite3
from header import show_header

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

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

st.title("Register for an account:")

def run_register(username, password):
    cursor.execute(
        "INSERT INTO users (username, password, fname, surname, email)"
        "VALUES (?, ?, ?, ?, ?)",
        (username, password, fName, sName, uniEmail)
    )

with st.form("register_form"):
    st.write("Register Form:")
    fName = st.text_input("First Name: ", placeholder = "First Name Here...")
    sName = st.text_input("Second Name: ", placeholder = "Surname Name Here...")
    username = st.text_input("Username: ", placeholder = "Username Here...")
    uniEmail = st.text_input("Email (university):", placeholder = "Uni email Here...")

    
    password = st.text_input("Password:", type = "password", placeholder = "Password Here...")

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Thank you for creating an account!")

# ---------------------------------------------------
# Return button
# ---------------------------------------------------
if st.button("Return to Login page"):
    st.switch_page("streamlit_app.py")