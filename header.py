import streamlit as st
import sqlite3
import os

def show_header():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0.5rem !important;
            }

            /* Fix column alignment */
            [data-testid="column"] {
                display: flex;
                align-items: center;
                justify-content: center;
            }

            div[data-testid="stButton"] button {
                background: none;
                border: solid;
                border-width: 2px;
                border-radius: 15px;
                font-weight: 400;
                color: gray !important;
                padding: 4px 16px;
                letter-spacing: 0.5px;
                margin-top: 10px;
                font-size: 20px ;
            }
            div[data-testid="stButton"] button:hover {
                color: #FF4B4B !important;
                background: none;
                border: solid;
                border-width: 2px;
            }
            hr {
                margin-top: 0rem !important;
                margin-bottom: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write("")  # small space at top

    avatar = "assets/default_avatar.png"

    if "user_id" in st.session_state:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT profile_picture FROM users WHERE id=?",
            (st.session_state["user_id"],)
        )

        result = cursor.fetchone()

        if result and result[0]:
            avatar = result[0]

    cols = st.columns([1,1.25,1.75,2,2,2,0.75,1.25,1,1])

    with cols[0]:
        st.write("")
        st.write("")
        avatar = "assets/page_icon.png"
        st.image(avatar, width=65)
    with cols[1]:
        st.write("")
        st.write("")
        if st.button("🏠  Home"):
            st.switch_page("pages/home_page.py")
    # inside show_header(), where cols[5] and cols[6] are for buttons
    with cols[3]:
        st.write("")
        st.write("")
        # Fetch user role from DB
        user_role = None
        user_admin = False
        if "user_id" in st.session_state:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT role, admin FROM users WHERE id=?", (st.session_state["user_id"],))
            result = cursor.fetchone()
            if result:
                user_role, user_admin = result
            conn.close()

        # Assignments tab for students
        if user_role == "Student":
            if st.button("📄  Assignments"):
                st.switch_page("pages/view_assignments.py")
        # Modules tab for lecturers
        elif user_role == "Lecturer":
            if st.button("📚  Modules"):
                st.switch_page("pages/view_modules.py")
        # Optionally admins see both
        elif user_admin:
            if st.button("💬  Assignments"):
                st.switch_page("pages/view_assignments.py")
            if st.button("📚  Modules"):
                st.switch_page("pages/view_modules.py")
    with cols[4]:
        st.write("")
        st.write("")
        if st.button("🏆  Leaderboard"):
            st.switch_page("pages/view_leaderboard.py")
    with cols[5]:
        st.write("")
        st.write("")
        if st.button("💬  Connect"):
            st.switch_page("pages/connect.py")
    with cols[6]:
        st.write("")
        st.write("")

        # Check if the current user is admin
        is_admin = False
        if "user_id" in st.session_state:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT admin FROM users WHERE id=?", (st.session_state["user_id"],))
            result = cursor.fetchone()
            if result and result[0] == 1:
                is_admin = True
            conn.close()

        # Show Admin button only if user is admin
        if is_admin:
            if st.button("⚒️"):
                st.switch_page("pages/admin_panel.py")
    with cols[7]:
        st.write("")
        st.write("")
        # Default theme
        if "theme" not in st.session_state:
            st.session_state.theme = "dark"

        if st.button("☀️  Theme"):
            if st.session_state.theme == "light":
                st.session_state.theme = "dark"
            else:
                st.session_state.theme = "light"

        if st.session_state.theme == "dark":
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

        elif st.session_state.theme == "light":
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #dbd9d9;
                    color: #0f0f0f;
                }

                h1, h2, h3, h4, h5, h6, p, span, label {
                    color: #0f0f0f !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
    
    with cols[8]:
        st.write("")
        st.write("")
        if st.button("Profile", key="profile_avatar_btn"):
            st.switch_page("pages/my_profile.py")

    with cols[9]:
        st.write("")
        st.write("")
        avatar = "assets/default_avatar.png"

        if "user_id" in st.session_state:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT profile_picture FROM users WHERE id=?",
                (st.session_state["user_id"],)
            )

            result = cursor.fetchone()

            if result and result[0] and os.path.exists(result[0]):
                avatar = result[0]

        st.image(avatar, width=65)

    st.divider()
