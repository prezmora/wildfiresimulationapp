import streamlit as st

def app():
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("Wildfire Prediction App")
    st.write("Welcome to the Wildfire Prediction App. Use the sidebar to navigate through the pages.")
