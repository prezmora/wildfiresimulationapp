import streamlit as st
from app import main

if __name__ == "__main__":
    if 'logged_in_user' not in st.session_state:
        st.session_state['logged_in_user'] = None
    main()
