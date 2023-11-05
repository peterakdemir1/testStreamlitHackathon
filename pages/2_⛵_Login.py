import streamlit as st
from dbconfig import *
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages

st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

placeholder = st.empty()

def verify(user_name_email, user_password):
    user = {'username': user_name_email, 'password': user_password} if '@' not in user_name_email else {'email': user_name_email, 'password': user_password}
    # print(user)
    fetchedUserList = users_dao.find_any(user)
    # print(fetchedUserList)
    if users_dao.find_any(user):
        st.session_state.username = fetchedUserList[0]['username']
        st.session_state.logged_in = True
        st.success('Successful Login!')
        show_pages(
            [
            Page("1_🏴‍☠️_Home.py", "Home", "🏴‍☠️"),
            # Page("pages/2_⛵_Login.py", "Login", "⛵"),
            Page("pages/3_❌_Play.py", "Play", "❌"),
            Page("pages/4_⚓_Profile.py", "Profile", "⚓"),
            # Page("pages/5_🧭_Register.py", "Register", "🧭"),
            Page("pages/6_🌊_Upload.py", "Upload", "🌊")
            ]
        )
        switch_page('Play')
    else:
        st.warning('Incorrect Username/Password.')

with placeholder.form("Login"):
    user_name_email = st.text_input('Username/Email')
    user_password = st.text_input('Password', type='password')
    clicked = st.form_submit_button("Login")
    
    if clicked:
        verify(user_name_email, user_password)
