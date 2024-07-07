import streamlit as st
from app import main, load_css


if __name__ == "__main__":
    print('assets/style.css')
    load_css('assets/style.css')
    if 'logged_in_user' not in st.session_state:
        st.session_state['logged_in_user'] = None
    main()
