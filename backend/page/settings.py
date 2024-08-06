import streamlit as st
from auth.user_utils import save_users, load_users

def show_settings_page(users_db):
    st.title('User Settings')

    email = st.session_state.user_email
    user_index = users_db["emails"].index(email)
    user = users_db["users"][user_index]

    with st.form(key='settings_form'):
        first_name = st.text_input('First Name', value=user.get('first_name', ''))
        last_name = st.text_input('Last Name', value=user.get('last_name', ''))
        update_button = st.form_submit_button(label='Update Settings')

    if update_button:
        users_db["users"][user_index]["first_name"] = first_name
        users_db["users"][user_index]["last_name"] = last_name
        save_users(users_db)
        st.success("Settings updated successfully!")

if __name__ == "__main__":
    users_db = load_users()
    show_settings_page(users_db)
