import streamlit as st
from auth.email_utils import send_verification_code
from auth.user_utils import register, complete_registration, login
from email_validator import validate_email, EmailNotValidError

def main():
    st.title("Wildfire Simulation App")

    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Tagline here")
    elif choice == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(email, password)
    elif choice == "Register":
        st.subheader("Register")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        locations = st.text_area("Locations (comma separated)")

        if password == confirm_password:
            if st.button("Register"):
                valid_email = False
                try:
                    validate_email(email)
                    valid_email = True
                except EmailNotValidError as e:
                    st.error(str(e))

                if valid_email:
                    locations_list = [loc.strip() for loc in locations.split(",")]
                    register(email, password, locations_list, send_verification_code)
        else:
            st.warning("Passwords do not match.")

    if st.session_state.get('registration_pending'):
        st.subheader("Verify Your Email")
        verification_input = st.text_input("Verification Code")
        if st.button("Verify"):
            complete_registration(verification_input)
