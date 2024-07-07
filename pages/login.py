import streamlit as st
from auth.user_utils import login

def login_page():
    st.title("Login")
    
    with st.form(key='login_form'):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Login')

    if submit_button:
        if login(email, password):
            st.session_state['logged_in'] = True
            st.experimental_set_query_params(page="dashboard")
            st.experimental_rerun()
