import streamlit as st
from auth.user_utils import load_users

# Page configuration
st.set_page_config(page_title="Wildfire Simulation Application", layout="wide")

# Load users from the JSON file
users_db = load_users()

# Initialize session state for user login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function to navigate
def navigate_to(page):
    st.experimental_set_query_params(page=page)
    st.experimental_rerun()

# Get the page from query params
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]

# Customize sidebar content
with st.sidebar:
    if st.session_state.logged_in:
        st.markdown(f"**Welcome, {st.session_state.user_email}!**")
        st.markdown("[Home](?page=home)")
        st.markdown("[Settings](?page=settings)")
        st.markdown("[Report](?page=report)")
        st.markdown("[Logout](?page=logout)")
    else:
        st.markdown("[Login](?page=login)")
        st.markdown("[Register](?page=register)")

# Page rendering
if page == 'home':
    st.title('Wildfire Simulation Application')
    if not st.session_state.logged_in:
        st.subheader("Please login or register to continue")

elif page == 'login':
    from pages.login import show_login_page
    show_login_page(users_db)

elif page == 'register':
    from pages.register import show_register_page
    show_register_page(users_db)

elif page == 'settings':
    if st.session_state.logged_in:
        from pages.v.settings import show_settings_page
        show_settings_page(users_db)
    else:
        st.error("Please log in to access settings.")
        st.markdown("[Login](?page=login)")

elif page == 'report':
    if st.session_state.logged_in:
        from pages.v.reports import show_report_page
        show_report_page(users_db)
    else:
        st.error("Please log in to view the report.")
        st.markdown("[Login](?page=login)")

elif page == 'logout':
    st.session_state.logged_in = False
    st.session_state.user_email = None
    navigate_to('home')
