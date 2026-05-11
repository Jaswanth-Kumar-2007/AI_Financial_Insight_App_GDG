import pyrebase

import streamlit as st

firebaseConfig = {
    "apiKey": st.secrets["FIREBASE_API_KEY"],
    "authDomain": st.secrets["FIREBASE_AUTH_DOMAIN"],
    "projectId": st.secrets["FIREBASE_PROJECT_ID"],
    "storageBucket": st.secrets["FIREBASE_STORAGE_BUCKET"],
    "messagingSenderId": st.secrets["FIREBASE_MESSAGING_SENDER_ID"],
    "appId": st.secrets["FIREBASE_APP_ID"],
    "databaseURL": st.secrets["FIREBASE_DATABASE_URL"]
}


firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()


def signup_user(email, password):

    try:

        user = auth.create_user_with_email_and_password(
            email,
            password
        )

        return user

    except:

        return None


def login_user(email, password):

    try:

        user = auth.sign_in_with_email_and_password(
            email,
            password
        )

        return user

    except:

        return None