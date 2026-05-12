from firebase_admin import auth
import streamlit as st


# ---------------- SIGNUP ----------------
def signup_user(email, password):

    try:
        user = auth.create_user(
            email=email,
            password=password
        )

        return {
            "uid": user.uid,
            "email": user.email
        }

    except Exception as e:
        print("Signup error:", e)
        return None


# ---------------- LOGIN ----------------
# NOTE: Firebase Admin SDK does NOT support password login
# So we only verify user exists

def login_user(email, password):

    try:
        user = auth.get_user_by_email(email)

        return {
            "uid": user.uid,
            "email": user.email
        }

    except Exception as e:
        print("Login error:", e)
        return None