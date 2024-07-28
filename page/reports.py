import streamlit as st
from auth.user_utils import load_users

def show_report_page(users_db):
    st.title('Report')

    if st.session_state.logged_in:
        st.write("User Information:")
        email = st.session_state.user_email
        user_index = users_db["emails"].index(email)
        user = users_db["users"][user_index]
        st.write(f"Email: {user['email']}")
        st.write(f"First Name: {user.get('first_name', 'N/A')}")
        st.write(f"Last Name: {user.get('last_name', 'N/A')}")
    else:
        st.error("Please log in to view the report.")

if __name__ == "__main__":
    users_db = load_users()
    show_report_page(users_db)
