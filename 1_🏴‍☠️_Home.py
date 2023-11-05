import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# from streamlit_extras.let_it_rain import rain
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.let_it_rain import rain


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

rain(
    emoji="🌊",
    font_size=54,
    falling_speed=8,
    animation_length="infinite",
)


st.markdown("<h1 style='text-align: center;'>TITLE</h1>", unsafe_allow_html=True)

st.markdown('''
Argh Matey! Explore the world to find me hidden treasures.

Sail to locations in user-uploaded images and collect the 7 treasures of the seven seas

Scan the locations and upload an image to collect me treasure!
''')

if not st.session_state.logged_in:
    if st.button("Login"):
        switch_page('login')

    if st.button("Register"):
        switch_page('register')
    show_pages (
        [
            Page("1_🏴‍☠️_Home.py", "Home", "🏴‍☠️"),
            Page("pages/2_⛵_Login.py", "Login", "⛵"),
            # Page("pages/3_❌_Play.py", "Play", "❌"),
            # Page("pages/4_⚓_Profile.py", "Profile", "⚓"),
            Page("pages/5_🧭_Register.py", "Register", "🧭"),
            # Page("pages/6_🌊_Upload.py", "Upload", "🌊")
        ]
    )
else:
    if st.button("Play"):
        switch_page("play")
    st.sidebar.markdown("Logged in as: " + st.session_state.username)
    log_out = st.sidebar.button("Log Out")
    if log_out:
        st.session_state.username = None
        st.session_state.logged_in = False
    show_pages (
        [
            Page("1_🏴‍☠️_Home.py", "Home", "🏴‍☠️"),
            # Page("pages/2_⛵_Login.py", "Login", "⛵"),
            Page("pages/3_❌_Play.py", "Play", "❌"),
            Page("pages/4_⚓_Profile.py", "Profile", "⚓"),
            # Page("pages/5_🧭_Register.py", "Register", "🧭"),
            Page("pages/6_🌊_Upload.py", "Upload", "🌊")
        ]
    )