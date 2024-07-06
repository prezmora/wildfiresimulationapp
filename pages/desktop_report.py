import streamlit as st

def app():
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("Desktop Report")
    st.write("Here you can view the desktop report.")
    # Add report components
