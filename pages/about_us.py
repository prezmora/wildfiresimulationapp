import streamlit as st

def app():
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("About Us")
    st.write("Information about the Wildfire Prediction App team.")
    # Add about us components
