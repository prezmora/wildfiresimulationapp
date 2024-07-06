import smtplib
import random
from email.message import EmailMessage
import os
import streamlit as st

def send_verification_code(email):
    code = random.randint(100000, 999999)
    msg = EmailMessage()
    msg.set_content(f"Your verification code is {code}")
    msg["Subject"] = "Your Verification Code"
    msg["From"] = os.environ.get("EMAIL_USER")  # Use your Gmail address
    msg["To"] = email

    try:
        server = smtplib.SMTP(os.environ.get("SMTP_SERVER"), os.environ.get("SMTP_PORT"))
        server.starttls()
        server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))  # Use your app password
        server.send_message(msg)
        server.quit()
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return None

    return code
