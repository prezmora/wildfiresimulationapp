import streamlit as st
from auth.user_utils import load_users

# Page configuration
st.set_page_config(page_title="Wildfire Simulation Application", layout="wide")

# Load users from the JSON file
users_db = load_users()

# Initialize session state for user login and page tracking
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'message' not in st.session_state:
    st.session_state.message = ''

if 'redirect' not in st.session_state:
    st.session_state.redirect = None

# Function to navigate
def navigate_to(page, message=None):
    if message:
        st.session_state.message = message
    st.session_state.redirect = page
    st.experimental_rerun()

# Get the page from query params
query_params = st.experimental_get_query_params()
if 'page' in query_params:
    st.session_state.page = query_params['page'][0]

# Display message if exists
if st.session_state.message:
    st.write(st.session_state.message)
    st.session_state.message = ''

# Handle redirection if set
if st.session_state.redirect:
    st.experimental_set_query_params(page=st.session_state.redirect)
    st.session_state.page = st.session_state.redirect
    st.session_state.redirect = None
    st.experimental_rerun()
    
# Add custom CSS
st.markdown("""
    <style>
    .nav-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        text-align: center;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border: none;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# Customize sidebar content
with st.sidebar:
    if st.session_state.logged_in:
        st.markdown(f"**Welcome, {st.session_state.user_email}!**")
        if st.button('Home'):
            navigate_to('home')
        if st.button('Settings'):
            navigate_to('settings')
        if st.button('Reports'):
            navigate_to('reports')
        if st.button('Logout'):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            navigate_to('home', message='You have been logged out.')
    else:
        if st.button('Login'):
            navigate_to('login')
        if st.button('Register'):
            navigate_to('register')

# Page rendering
page = st.session_state.page

if page == 'home':
    st.title('Wildfire Simulation Application')
    if not st.session_state.logged_in:
        st.subheader("Please login or register to continue")

elif page == 'login':
    from page.login import show_login_page
    show_login_page(users_db)

elif page == 'register':
    from page.register import show_register_page
    show_register_page(users_db)

elif page == 'settings':
    if st.session_state.logged_in:
        from page.settings import show_settings_page
        show_settings_page(users_db)
    else:
        st.error("Please log in to access settings.")
        navigate_to('login')

elif page == 'reports':
    if st.session_state.logged_in:
        from page.reports import show_report_page
        show_report_page(users_db)
    else:
        st.error("Please log in to view the report.")
        navigate_to('login')

elif page == 'logout':
    st.session_state.logged_in = False
    st.session_state.user_email = None
    navigate_to('home')
