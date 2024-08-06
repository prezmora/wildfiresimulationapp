import streamlit as st
from auth.user_utils import load_users

def home():
    st.title("Home")
    st.write("Wildfire Simulation Applications")
    st.write(st.session_state['logged_in'])
    if not st.session_state['logged_in']:
        st.subheader("Please login or register to continue on the wildfire simulation.")

        if st.button("Login"):
            st.experimental_set_query_params(page="login")
            st.experimental_rerun()
        if st.button("Register"):
            st.experimental_set_query_params(page="register")
            st.experimental_rerun()
