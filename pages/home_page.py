import streamlit as st

st.Page("pages/home_page.py")

st.set_page_config(
    page_title="Assignment Tracker",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Assignment Tracker. Made by Aparna, Tabitha, Tristan."
    }
)

#st.markdown("<h2 style='text-align: right;'>👤</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col2:
    if st.button("👤"):
        st.switch_page(st.Page("pages/my_profile.py"))

st.divider()
st.markdown("<h1 style='text-align: center;'>Homepage</h1>", unsafe_allow_html=True)
st.write("") 
st.write("") 
st.write("Welcome to the Assignment Tracker App! This app is designed to help you stay organized and on top of your assignments. You can view your assignments, check the leaderboard, and connect with others. Let's get started!")
st.title("Your overall progress")
progress = st.progress(0)

for i in range(100):
    progress.progress(i + 1)

st.success("Assignments all completed!")

st.write("")
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("View Assignments"):
     st.switch_page(st.Page("pages/view_assignments.py"))
with col2:
    if st.button("View Leaderboard"):
     st.switch_page(st.Page("pages/view_leaderboard.py"))
with col3:
    if st.button("Connect"):
     st.switch_page(st.Page("pages/connect.py"))


st.write("")
st.write("")

st.write("Assignment Tracker helps you stay organised by keeping all your tasks and deadlines in one place. Add your assignments, track your progress, and never miss a due date again. Whether you're juggling multiple subjects or just need a little extra help staying on top of things, this app has got you covered.")

st.write("")

st.write("With Assignment Tracker, you can easily add new assignments, set due dates, and mark tasks as complete. Stay on top of your workload and never feel overwhelmed again. Our simple and clean interface makes it easy to see exactly what needs to be done and when.Whether you're a student managing coursework or just someone who wants to stay productive, Assignment Tracker is designed to make your life easier. Track multiple subjects, view your progress, and celebrate when everything is done. Your deadlines are our priority.")
st.write("")
st.divider()
st.balloons()



