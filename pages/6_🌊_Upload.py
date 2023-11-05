import streamlit as st
import base64
import sys
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
from functions import *
import io
from dbconfig import *
from streamlit_image_select import image_select
from PIL import Image
sys.path.append('..')

treasure_files = [f'treasures/{i+1}.png' for i in range(7)]
treasures = {'1':"🏴‍☠️",'2':"⛵",'3':"❌",'4':"⚓",'5':"🧭",'6':"🌊",'7':"🦜"}



st.markdown("<h1 style='text-align: center;'>Upload Challenge</h1>", unsafe_allow_html=True)
st.sidebar.markdown("Logged in as: " + st.session_state.username)
log_out = st.sidebar.button("Log Out")


# if "uploaded" not in st.session_state:
#     st.session_state.uploaded = False

# if not st.session_state.uploaded:
uploaded_file = st.file_uploader("Choose an image", type=["png","jpg"])

if uploaded_file is not None:
    # Display the uploaded image as HTML
    # Read the image file as bytes
    image_bytes = uploaded_file.read()
    # image_bytes = Image.resize(image_bytes, (300, 300))
    # Encode the image bytes as base64
    image_base64 = base64.b64encode(image_bytes).decode()
    st.markdown(f'<img src="data:image/png;base64,{image_base64}" alt="Uploaded Image" style="width: 600px; height: auto;">', unsafe_allow_html=True)
    selection = image_select(
        "Select a Treasure:",
        images=treasure_files,
        return_value="original"
    )

    reward = treasures[selection.split('.')[0][-1]]

    riddle = st.text_input("Riddle:")

submit_button = st.button("Submit")

if submit_button:
    if uploaded_file is not None:
        gps_info = get_gps_info(image_base64)
        coordinates = get_coords(gps_info)

        # insert into mongo
        image_data = {
            "username": st.session_state.username,
            "image_bytes": image_bytes,
            "riddle": riddle,
            "reward": reward,
            "coordinates": coordinates
        }

        try:
            images_dao.insert_one(image_data)
            st.success(f'Successfully Uploaded: {uploaded_file.name}')
            st.session_state.uploaded = True

        except:
            st.error(f'Failed Upload: {uploaded_file.name}')

    else:
        st.warning("Please upload a file before submitting.")
# else:
#     submit_another = st.button("Submit another image")
#     uploaded_file = None

#     if submit_another:
#         st.session_state.uploaded = False

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