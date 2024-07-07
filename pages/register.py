import streamlit as st
from auth.user_utils import register, complete_registration
from auth.email_utils import send_verification_code
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[a-zA-Z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

def register_page():
    if 'registration_pending' in st.session_state and st.session_state['registration_pending']:
        st.subheader("Verify Your Email")
        verification_input = st.text_input("Verification Code")
        if st.button("Verify"):
            if complete_registration(verification_input):
                st.experimental_set_query_params(page="login")
                st.experimental_rerun()
    else:
        st.subheader("Register")
        with st.form(key='register_form'):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Your Password", type="password")
            locations = st.text_area("Locations (comma separated)")
            
            submit_button = st.form_submit_button(label='Register')

        if submit_button:
            print(email, password, confirm_password, locations)
            # if password != confirm_password:
            #     st.warning("Passwords do not match.")
            # else:
            #     if not validate_email(email):
            #         st.warning("Invalid email address.")
            #     else:
            #         valid_password, password_message = validate_password(password)
            #         if not valid_password:
            #             st.warning(password_message)
            #         else:
            #             if register(email, password, [loc.strip() for loc in locations.split(",")], send_verification_code):
            #                 st.experimental_rerun()
