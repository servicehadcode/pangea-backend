import requests
from flask import current_app, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from services.mongo_service import mongo_service
from datetime import datetime

def log_user_activity(user_data, activity_type):
        activity_record = {
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "activity": activity_type,
            "timestamp": datetime.utcnow()  # Or datetime.utcnow()
        }
        mongo_service.db.activity_logs.insert_one(activity_record)
        print(f"Logged activity: {activity_record}")

class GitHubAuthService:
    def __init__(self):
        self.oauth = OAuth(current_app)
        self.github = self.oauth.register(
            name='github',
            client_id=current_app.config['GITHUB_CLIENT_ID'],
            client_secret=current_app.config['GITHUB_CLIENT_SECRET'],
            access_token_url='https://github.com/login/oauth/access_token',
            authorize_url='https://github.com/login/oauth/authorize',
            api_base_url='https://api.github.com/',
            client_kwargs={'scope': 'user:email'},
        )

    def authorize_redirect(self):
        # Before redirecting to GitHub for authorization, log the activity
        if 'user' in session:  # Check if there's a user already logged in
            user_data = session['user']  # User data stored in session
            log_user_activity(user_data, "authorize_redirect")  # Log the activity
        return self.github.authorize_redirect(url_for('auth.github_callback', _external=True))

    def get_user_info(self):
        # After successful authorization, log the login activity
        token = self.github.authorize_access_token()
        resp = self.github.get('user', token=token)
        
        user_info = {
            'github_id': str(resp.json().get('id')),
            'username': resp.json().get('login'),
            'email': resp.json().get('email'),
            'avatar_url': resp.json().get('avatar_url')
        }

        # Log the login activity (successful login via GitHub)
        log_user_activity(user_info, "login")  # Activity type: "login"

        return user_info

    def handle_logout(self):
        # Check if the user data exists in the session
        user_data = session.get('user')  # Assuming user data is stored in session
        if user_data:
            # Log the logout activity if user data is available
            log_user_activity(user_data, "logout")
        else:
            # If there's no user data, log it or handle the error gracefully
            print("No user data found in session for logout.")
        
        # Clear the session after logging out
        session.clear()  # Ensure session is cleared properly