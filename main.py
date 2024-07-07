import streamlit as st
from pages.home import home
from pages.login import login_page
from pages.register import register_page

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_bootstrap():
    st.markdown("""
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

def main():
    load_bootstrap()
    load_css('assets/style.css')

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    def set_page(page_name):
        st.session_state['page'] = page_name
        st.experimental_set_query_params(page=page_name)

    # Sidebar menu
    if st.session_state['logged_in']:
        menu = ["Home", "Dashboard", "Settings", "Logout"]
        icons = ["fas fa-home", "fas fa-tachometer-alt", "fas fa-cogs", "fas fa-sign-out-alt"]
    else:
        menu = ["Home", "Login", "Register"]
        icons = ["fas fa-home", "fas fa-sign-in-alt", "fas fa-user-plus"]

    sidebar_html = """
    <div class="sidebar-content">
        {links}
    </div>
    """.format(links="".join([
        f'<div class="sidebar-item"><button class="sidebar-button" onclick="window.location.href=\'/?page={item.lower()}\'"><i class="{icons[idx]} icon"></i> {item}</button></div>'
        for idx, item in enumerate(menu)
    ]))

    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)

    # Hide Streamlit's built-in sidebar
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                width: 0;
                padding: 0;
                overflow: hidden;
            }
            [data-testid="stSidebar"][aria-expanded="true"] > div:first-child .element-container {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Get the page from session state
    page = st.experimental_get_query_params().get('page', ['home'])[0]

    # Set the page based on the session state
    if page == 'home':
        home()
    elif page == 'login':
        login_page()
    elif page == 'register':
        register_page()
    elif page == 'logout':
        st.session_state['logged_in'] = False
        set_page('home')
        st.experimental_rerun()
    elif page == 'dashboard':
        st.write("Welcome to the Dashboard")
    elif page == 'settings':
        st.write("Settings Page")

if __name__ == "__main__":
    main()
