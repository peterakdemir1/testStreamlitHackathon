import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# from streamlit_extras.let_it_rain import rain
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.let_it_rain import rain
from dbconfig import users_dao, images_dao#, solved_dao

user = {"username": st.session_state.username}
user_treasures = users_dao.find_any(user)[0]['treasures']

# user_images = solved_dao.find_any(user)
# print("\n\n\n LOOK HERE: ", user_images)
p1 = user_treasures['1']
p2 = user_treasures['2']
p3 = user_treasures['3']
p4 = user_treasures['4']
p5 = user_treasures['5']
p6 = user_treasures['6']
p7 = user_treasures['7']

st.markdown("<h1 style='text-align: center;'>Profile</h1>", unsafe_allow_html=True)
st.sidebar.markdown("Logged in as: " + st.session_state.username)
log_out = st.sidebar.button("Log Out")

st.markdown(f'''
<h2>{st.session_state.username} Statistics<h2><h3>Rewards</h3>
<p>🏴‍☠️: {p1} found!</p>
<p>⛵: {p2} found!</p>
<p>❌: {p3} found!</p>
<p>⚓: {p4} found!</p>
<p>🧭: {p5} found!</p>
<p>🌊: {p6} found!</p>
<p>🦜: {p7} found!</p>
<br>

<h3>Found Treasures!</h3>
<p>Put each image here</p>
''', unsafe_allow_html=True)

if log_out:
    st.session_state.logged_in = False
    st.session_state.username = None
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
    switch_page("Home")

# for image in user_images:
#     selected_image = image["image_bytes"]
#     # print(selected_image)
#     st.markdown(f'<img src="data:image/png;base64,{selected_image}" alt="Uploaded Image" style="width: 300px; height: auto;">', unsafe_allow_html=True)