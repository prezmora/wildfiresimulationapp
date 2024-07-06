import streamlit as st

def app():
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("Login")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success("Logged in successfully")
