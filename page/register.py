import streamlit as st
from auth.user_utils import register_user

def show_register_page(users_db):
    st.title('User Registration')

    with st.form(key='register_form'):
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        submit_button = st.form_submit_button(label='Register')

    if submit_button:
        if len(password) < 8:
            st.error("Password must be at least 8 characters long.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, message = register_user(users_db, email, password)
            if success:
                st.success(message)
                navigate_to('login')
            else:
                st.error(message)

def navigate_to(page):
    st.experimental_set_query_params(page=page)
    st.experimental_rerun()

if __name__ == "__main__":
    users_db = load_users()
    show_register_page(users_db)
