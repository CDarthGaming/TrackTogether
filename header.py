import streamlit as st

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
                border: none;
                font-weight: 800;
                color: white !important;
                padding: 8px 16px;
                letter-spacing: 0.5px;
                margin-top: 10px;
            }
                
            div[data-testid="stButton"] button p {
                font-size: 20px ;
            }
            div[data-testid="stButton"] button:hover {
                color: #FF4B4B !important;
                background: none;
                border: none;
            }
            hr {
                margin-top: 0rem !important;
                margin-bottom: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write("")  # small space at top

    col1, col2, col3, col4, col5 = st.columns([1.5, 0.75, 1, 1, 1])

    with col1:
        st.image("page_icon.png", width=90)
    with col2:
        if st.button("🏠  Home"):
            st.switch_page("streamlit_app.py")
    with col3:
        if st.button("📋  Assignments"):
            st.switch_page("pages/view_assignments.py")
    with col4:
        if st.button("🏆  Leaderboard"):
            st.switch_page("pages/view_leaderboard.py")
    with col5:
        if st.button("👤 Profile"):
            st.switch_page("pages/my_profile.py")

    st.divider()
