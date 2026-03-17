import streamlit as st
import sqlite3
import bcrypt
import time
import os
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

# ---------------------------------------------------
# Session check
# ---------------------------------------------------
if "user_id" not in st.session_state:
    st.switch_page("streamlit_app.py")

user_id = st.session_state["user_id"]

# ---------------------------------------------------
# Database connection
# ---------------------------------------------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT username, fName, surname, email, profile_picture FROM users WHERE id = ?",
    (user_id,)
)

user = cursor.fetchone()

if not user:
    st.error("Your record cannot be found!")
    st.stop()

username_in, first_name_in, second_name_in, email_in, pic = user

# ---------------------------------------------------
# Profile header
# ---------------------------------------------------
cols = st.columns([1,4,1])

avatar_path = "assets/default_avatar.png"

if pic and os.path.exists(pic):
    avatar_path = pic

cols[0].image(avatar_path, width=150)

with cols[1]:
    st.header(f"Hello {username_in}")
    st.caption("Manage your profile settings")

st.divider()

# ---------------------------------------------------
# Profile form
# ---------------------------------------------------
with st.form("profile_form"):

    st.subheader("Update Profile")

    uploaded_file = st.file_uploader(
        "Upload Profile Picture",
        type=["png","jpg","jpeg"]
    )

    if uploaded_file:
        st.image(uploaded_file, width=120)

    username = st.text_input("Username", value=username_in)
    first_name = st.text_input("First Name", value=first_name_in)
    second_name = st.text_input("Surname", value=second_name_in)
    email = st.text_input("Email", value=email_in)

    new_password = st.text_input("New Password", type="password")
    st.caption("Leave blank if you do not want to change your password.")

    submitted = st.form_submit_button("Update Profile")

    if submitted:

        if not all([username, first_name, second_name, email]):
            st.warning("All fields must be filled.")
            st.stop()

        if not email.endswith("@lancashire.ac.uk"):
            st.warning("You must use a University of Lancashire email.")
            st.stop()

        # Save profile picture
        if uploaded_file:
            file_path = f"uploads/user_{user_id}.png"

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            cursor.execute(
                "UPDATE users SET profile_picture=? WHERE id=?",
                (file_path, user_id)
            )

        # Password update
        if new_password:
            hashed_password = bcrypt.hashpw(
                new_password.encode(),
                bcrypt.gensalt()
            ).decode()

            cursor.execute(
                """
                UPDATE users
                SET username=?, password=?, fName=?, surname=?, email=?
                WHERE id=?
                """,
                (
                    username,
                    hashed_password,
                    first_name,
                    second_name,
                    email,
                    user_id,
                ),
            )

        else:
            cursor.execute(
                """
                UPDATE users
                SET username=?, fName=?, surname=?, email=?
                WHERE id=?
                """,
                (
                    username,
                    first_name,
                    second_name,
                    email,
                    user_id,
                ),
            )

        conn.commit()

        st.toast("Your profile has been updated!", icon="👾")

        time.sleep(1)
        st.rerun()

# ---------------------------------------------------
# Delete Account Form
# ---------------------------------------------------
st.divider()

with st.form("delete_profile_form"):
    
    st.subheader("Delete Profile")

    st.warning("Deleting your account will permanently remove all your data.",icon="⚠️")

    confirm_delete = st.checkbox("I understand this action cannot be undone")

    if st.form_submit_button("Delete My Account"):
        if confirm_delete:

            assignments_conn = sqlite3.connect("assignments.db")
            assignments_cursor = assignments_conn.cursor()

            # Delete tasks linked to the user's assignments
            assignments_cursor.execute("""
                DELETE FROM tasks
                WHERE assignment_id IN (
                    SELECT id FROM assignments WHERE user_id=?
                )
            """, (user_id,))

            # Delete the user's assignments
            assignments_cursor.execute(
                "DELETE FROM assignments WHERE user_id=?",
                (user_id,)
            )

            assignments_conn.commit()
            assignments_conn.close()

            # Delete the user account
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            conn.close()

            st.success("Your account has been deleted.")

            time.sleep(2)

            st.session_state.clear()

            st.switch_page("streamlit_app.py")

        else:
            st.warning("Please confirm account deletion first!", icon="🚨")


if st.button("Log Out"):
    st.session_state.clear()
    st.switch_page("streamlit_app.py")