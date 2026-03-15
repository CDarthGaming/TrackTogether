import streamlit as st
import pandas as pd
import sqlite3
import sys
sys.path.append(".")
from header import show_header
 
# Sets the page layout.
st.set_page_config(
    page_title="Assignment Tracker",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Assignment Tracker. Made by Aparna, Tabitha, Tristan."
    }
)
 
show_header()
 
# Gets the user ID from the session storage.
user_id = st.session_state.get("user_id")

if (user_id == None):
    st.switch_page("streamlit_app.py") 

# Connect to users database to get username
users_conn = sqlite3.connect("users.db")
cursor = users_conn.cursor()
cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
user = cursor.fetchone()
users_conn.close()
 
if user:
    username = user[0]
    st.markdown(f"<h2 style='text-align: center;'>Welcome, {username}!</h2>", unsafe_allow_html=True)
 
st.title("Choose Module Chat:")
st.write("")
 
# Connect to assignments database
assign_conn = sqlite3.connect("assignments.db")
cursor2 = assign_conn.cursor()
 
# Get distinct modules for this user
cursor2.execute("SELECT DISTINCT module_name, module_code FROM assignments WHERE user_id = ?", (user_id,))
modules = cursor2.fetchall()
assign_conn.close()
 
if not modules:
    st.info("No modules found! Add some assignments first.")
else:
    for module in modules:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"📚 {module[0]} — {module[1]}")
        with col2:
            if st.button("Open Chat", key=f"chat_{module[1]}"):
                st.session_state["module_code"] = module[1]
                st.switch_page("pages/chat_message.py")