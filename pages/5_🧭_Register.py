import streamlit as st
from hacknjit2023_models.user import User
from dbconfig import users_dao, images_dao

st.markdown("<h1 style='text-align: center;'>Register</h1>", unsafe_allow_html=True)

def register_account(register_username, register_email, register_password):
	if register_username and register_email and register_password:
		currUser = User(
			username = register_username,
			email = register_email,
			password = register_password,
			treasures = {
				"1":0,
				"2":0,
				"3":0,
				"4":0,
				"5":0,
				"6":0,
				"7":0
			}
		)
		
		if not users_dao.find_any({'username': register_username}) and not users_dao.find_any({'email': register_email}): # new account
			users_dao.insert_one(currUser.__dict__)
			st.success("Account Created!")
		else:
			st.warning("Account Already Exists")
	else:
		st.warning("Username/Email already exists or incomplete")
					
with st.form("Register"):
	register_username = st.text_input('Username')
	register_email = st.text_input('Email')
	register_password = st.text_input('Password', type='password')
	account = st.form_submit_button('Register')
	
if account:
	register_account(register_username, register_email, register_password)  
        # st.write("registered", register_username)