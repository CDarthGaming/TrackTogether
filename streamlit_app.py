import streamlit as st
import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

def check_users(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", 
        (username, password)
    )

    user = cursor.fetchone()
    return user

def login_page():
    st.title("Welcome to your assignment tracker, please login below!")

    with st.form("login_form"):
        st.write("Login Form:")
        username = st.text_input("Username", placeholder = "First Name Here...")
        password = st.text_input("Password:", type = "password", placeholder = "Password Here...")

        submitted = st.form_submit_button("Submit")

        createAccount = st.form_submit_button("Click to create an account!")
        
        if createAccount:
            st.switch_page(st.Page("pages/create_account.py"))

        if submitted:
            user = check_users(username, password)

            if user:
                st.success("Login successful!")

                st.session_state['user'] = {
                    'id': user[0],
                    'username': user[1],
                    'password': user[2],
                    'first_name': user[3],
                    'second_name': user[4],
                    'email': user[5]
                }

                st.switch_page(st.Page("pages/home_page.py"))
            else:
                st.error("Invalid username or password")


login_page()

