import streamlit as st
from PIL import Image
import base64
import streamlit.components.v1 as components
from streamlit_extras.switch_page_button import switch_page
# from streamlit_extras.let_it_rain import rain
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.let_it_rain import rain
import functions as fn
import math
from dbconfig import users_dao, images_dao#, solved_dao
import random

def dms_to_dd(degrees, minutes, seconds, direction):
    dd = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'W']:
        dd *= -1
    return dd

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

treasures_dict = {"🏴‍☠️": '1', "⛵": '2', "❌": '3', "⚓": '4', "🧭": '5', "🌊": '6', "🦜": '7'}

st.markdown("<h1 style='text-align: center;'>Play Challenge</h1>", unsafe_allow_html=True)
st.sidebar.markdown("Logged in as: " + st.session_state.username)
log_out = st.sidebar.button("Log Out")        
image_obj = images_dao.find_any()

# Check if the 'target_image' key exists in the session state
if 'target_image' not in st.session_state or st.button("Next"):
    # Get a new image, riddle, and reward from the database, cycle through
    # If the image was created by the user, skip
    index = random.randint(0, len(image_obj) - 1)
    st.session_state.target_image = image_obj[index]["image_bytes"]
    st.session_state.riddle = image_obj[index]["riddle"]
    st.session_state.reward = image_obj[index]["reward"]
    st.session_state.target_coords = image_obj[index]["coordinates"]
    # These lines seem to be for testing purposes and should be removed or commented out
    # riddle = "riddle2"
    # reward = "🟨"

# Use the image from the session state
target_image = st.session_state.target_image
riddle = st.session_state.riddle
reward = st.session_state.reward
target_coords = st.session_state.target_coords

st.markdown('# Find the treasure!')
# st.image(target_image)
st.markdown(f'<img src="data:image/png;base64,{target_image}" alt="Uploaded Image" style="width: 200px; height: auto;">', unsafe_allow_html=True)
st.markdown(f'### Riddle:\n{riddle}')
st.markdown(f'Reward: {reward}')

uploaded_file = st.file_uploader("Found the treasure? Upload an image of it to complete the challenge!", type=["png","jpg"])

if uploaded_file is not None:
    # Display the uploaded image as HTML
    # Read the image file as bytes
    image_bytes = uploaded_file.read()
    # Encode the image bytes as base64
    image_base64 = base64.b64encode(image_bytes).decode()

submit_button = st.button("Submit")

if submit_button:
    if uploaded_file is not None:
        # convert to Base64
        bytes_data = uploaded_file.getvalue()
        image_base64 = base64.b64encode(bytes_data).decode()
        # st.markdown(result)
        st.markdown(f'<img src="data:image/png;base64,{image_base64}" alt="Uploaded Image" style="width: 200px; height: auto;">', unsafe_allow_html=True)
        gps_info = fn.get_gps_info(image_base64)
        coordinates = fn.get_coords(gps_info)

        # First point
        lat1 = dms_to_dd(target_coords["latitude"]["degrees"], target_coords["latitude"]["minutes"], target_coords["latitude"]["seconds"], target_coords["latitude"]["direction"])
        lon1 = dms_to_dd(target_coords["longitude"]["degrees"], target_coords["longitude"]["minutes"], target_coords["longitude"]["seconds"], target_coords["longitude"]["direction"])

        # Second point
        lat2 = dms_to_dd(coordinates["latitude"]["degrees"], coordinates["latitude"]["minutes"], coordinates["latitude"]["seconds"], coordinates["latitude"]["direction"])
        lon2 = dms_to_dd(coordinates["longitude"]["degrees"], coordinates["longitude"]["minutes"], coordinates["longitude"]["seconds"], coordinates["longitude"]["direction"])

        distance_km = haversine(lat1, lon1, lat2, lon2)
        similarity = fn.calc_cosine_similarity(fn.extract_features(image_base64), fn.extract_features(base64.b64encode(target_image).decode()))
        if similarity >= 0.55 and distance_km <= 0.1:
            st.markdown(f"## Congrats! You found the treasure! {reward}")
            solve_data = {
                "username": st.session_state.username,
                "image_bytes": target_image,
            }
            try:
                # solved_dao.insert_one(solve_data)
                # users_dao.insert
                old_treasures = users_dao.find_any({'username': st.session_state.username})[0]['treasures']
                old_treasures[treasures_dict[reward]] += 1
                updated_user = {
                    'username': st.session_state.username,
                    'treasurers': old_treasures
                }
                users_dao.update_one(updated_user)
                st.success(f'Successfully obtained the reward!')
            except:
                st.error(f'Failed uploading your success...')
        else:
            st.markdown("## Argg... It doesn't seem like you found the treasure yet!")
        st.markdown(f'Image Similarity: {similarity*100}%')
        st.markdown(f'Distance From Treasure: {distance_km * 1000} meters')

        # insert into mongo
        # image_data = {
        #     "username": st.session_state.username,
        #     "img_bson": bytes_data,
        #     "coordinates": result
        # }

        # try:
        #     images_dao.insert_one(image_data)
        #     st.success(f'Successfully Uploaded: {uploaded_file.name}')
        # except:
        #     st.error(f'Failed Upload: {uploaded_file.name}')

    else:
        st.warning("Please upload a file before submitting.")

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