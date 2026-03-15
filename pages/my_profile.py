import streamlit as st
import sqlite3
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

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

user_id = st.session_state['user_id']

if 'user_id' not in st.session_state:
      st.switch_page("streamlit_app.py")

cursor.execute("SELECT username, password, fName, surname, email FROM users WHERE id = ?", (user_id,))
user = cursor.fetchone()

if not user:
      st.error("Your record cannot be found!")
      st.stop()


username_in, password_in, first_name_in, second_name_in, email_in = user

with st.form("profile_form"):
        st.write("My Profile:")
        username = st.text_input("Username", value = username_in)
        password = st.text_input("Password:", type = "password", value = password_in)
        first_name = st.text_input("First Name:", value = first_name_in)
        second_name = st.text_input("Second Name:",value = second_name_in)
        email = st.text_input("Email:", value = email_in)

        submitted = st.form_submit_button("Submit")

        if submitted:
               cursor.execute("UPDATE users SET username = ?, password = ?, fName = ?, surname = ?, email = ? WHERE id = ?", (username, password, first_name, second_name, email, user_id))
               conn.commit()
               st.toast(body="Your profile has been updated!",icon="👾")
            
