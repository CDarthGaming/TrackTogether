import streamlit as st
import sqlite3
import bcrypt

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
st.write("Please login below.")
st.caption("If you created an account before 17/03/2026, you will have to create a new student account.")

# Connect to users database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

def check_user(username, password):
    cursor.execute("SELECT id, username, password, fName, surname, email, role, admin, approved, course_id, year FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        return None
    
    user_id, db_username, db_password, fName, sName, email, role, admin, approved, course_id, year = user
    
    if bcrypt.checkpw(password.encode(), db_password.encode()):
        return {
            "id": user_id,
            "username": db_username,
            "fname": fName,
            "surname": sName,
            "email": email,
            "role": role,
            "admin": admin,
            "approved": approved,
            "course_id": course_id,
            "year": year
        }
    else:
        return None

with st.form("login_form"):
    username = st.text_input("Username", placeholder="Username here...")
    password = st.text_input("Password", type="password", placeholder="Password here...")
    
    submitted = st.form_submit_button("Login")
    
    if submitted:
        user = check_user(username, password)
        
        if not user:
            st.error("Invalid username or password.")
        else:
            # Handle lecturer approval
            if user["role"] == "Lecturer" and not user["approved"]:
                st.warning("Your lecturer account is pending admin approval. Please wait.",icon="⚠️")
            else:
                # Login success
                st.session_state["user_id"] = user["id"]
                st.session_state["user"] = user
                # Default theme
                if "theme" not in st.session_state:
                    st.session_state["theme"] = "dark"
                
                st.success(f"Login successful! Welcome, {user['fname']}.")
                st.switch_page("pages/home_page.py")

# ---------------------------------------------------
# Create an account button
# ---------------------------------------------------
if st.button("Create an account"):
    st.switch_page("pages/create_account.py")