import streamlit as st
import sqlite3
import pandas as pd
from header import show_header

conn = sqlite3.connect("users.db", check_same_thread=False)

userID = st.session_state.get("user_id")

if (userID == None):
    st.switch_page("streamlit_app.py")

username_query = """
SELECT username
FROM users
WHERE id = ?
"""

name_df = pd.read_sql_query(username_query, conn, params=(userID,))

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

if not name_df.empty:
    username = name_df.iloc[0]

    st.markdown(f"<h1 style='text-align: center;'>Welcome to Track Together {username['username']}</h1>", unsafe_allow_html=True)

st.write("") 
st.write("") 

topTextCols = st.columns([2.5,8,2.5])

conn = sqlite3.connect("assignments.db", check_same_thread=False)

query = """
SELECT progress
FROM assignments
WHERE user_id = ?
"""

df = pd.read_sql_query(query, conn, params=(userID,))

if not df.empty:
    overall_progress = int(df["progress"].mean())
else:
    overall_progress = 0

topTextCols[1].title("Your overall progress")

topTextCols[1].progress(overall_progress)

topTextCols[1].markdown(f"{overall_progress}% complete")

if overall_progress == 100:
    st.success("🎉 All assignments completed!")
    st.balloons()

st.write("")
st.write("")

cols = st.columns([3.2,4.4,4.4,4.4])

st.write("")
st.write("")

bottomTextCols = st.columns([2.5,8,2.5])

bottomTextCols[1].write("Welcome to the Track Together website! This website is designed to help you stay organized and on top of your assignments. You can view your assignments, check the leaderboard, and connect with others.")

st.write("")

bottomTextCols[1].write("Assignments are linked to your account, so you can easily see your own workload and how far through it you are. As you update progress or complete assignments, your overall completion will increase.")

st.write("")

bottomTextCols[1].write("You can also check the Leaderboard to see how your progress compares with other users. It’s a simple way to stay motivated and keep moving forward with your work.")

st.write("")
st.divider()

st.caption("Version 1.1.2")