import streamlit as st
from auth.user_utils import authenticate_user

def show_login_page(users_db):
    st.title('User Login')

    with st.form(key='login_form'):
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        login_button = st.form_submit_button(label='Login')

    if login_button:
        if authenticate_user(users_db, email, password):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Login successful!")
            navigate_to('home')
        else:
            st.error("Invalid email or password.")

def navigate_to(page):
    st.experimental_set_query_params(page=page)
    st.experimental_rerun()

if __name__ == "__main__":
    users_db = load_users()
    show_login_page(users_db)
