import firebase_admin # type:ignore
from firebase_admin import credentials, firestore

firebase_config = {
    "apiKey": "AIzaSyABbJZXsNSBh36jCrG3nE8CT9HUtsQnfgI",
    "authDomain": "sigtrack-chat-attempt.firebaseapp.com",
    "databaseURL": "https://sigtrack-chat-attempt-default-rtdb.firebaseio.com/",
    "projectId": "sigtrack-chat-attempt",
    "storageBucket": "sigtrack-chat-attempt.firebasestorage.app",
    "messagingSenderId": "117009312015",
    "appId": "1:117009312015:web:2369d060008afb089f367a",
}


# Path to your service account key file (downloaded from Firebase Console)
path = credentials.Certificate("sigtrack/chat/firebase_config.json")
firebase_admin.initialize_app(path)

# Initialize Firestore
db = firestore.client()
