import os
import random
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

def send_verification_code(email):
    verification_code = str(random.randint(100000, 999999))
    st.session_state['verification_code'] = verification_code

    try:
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

        msg = MIMEText(f"Your verification code is: {verification_code}")
        msg["Subject"] = "Email Verification Code"
        msg["From"] = smtp_user
        msg["To"] = email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())

        return True
    except Exception as e:
        st.error(f"Failed to send verification code: {e}")
        return False
