from flask import current_app, session, url_for
from authlib.integrations.flask_client import OAuth
from services.mongo_service import mongo_service

def log_user_activity(user_data, activity_type):
    from models.user_activity_model import create_user_activity
    from flask import current_app

    try:
        # Check if MongoDB service is initialized
        db_initialized = mongo_service.db is not None
        user_activity_initialized = mongo_service.user_activity is not None

        if hasattr(current_app, 'logger'):
            current_app.logger.info(f"MongoDB initialization status: db={db_initialized}, user_activity={user_activity_initialized}")
        else:
            print(f"MongoDB initialization status: db={db_initialized}, user_activity={user_activity_initialized}")

        if db_initialized and user_activity_initialized:
            # Use the same collection as in auth_controller
            activity_record = create_user_activity(user_data, activity_type)

            # Log the activity record for debugging
            if hasattr(current_app, 'logger'):
                current_app.logger.info(f"Activity record to insert: {activity_record}")
            else:
                print(f"Activity record to insert: {activity_record}")

            # Insert the record
            result = mongo_service.user_activity.insert_one(activity_record)

            # Log the result
            if hasattr(current_app, 'logger'):
                current_app.logger.info(f"Logged activity with ID: {result.inserted_id}")
            else:
                print(f"Logged activity with ID: {result.inserted_id}")

            # Verify the document was inserted
            verification = mongo_service.user_activity.find_one({"_id": result.inserted_id})
            if hasattr(current_app, 'logger'):
                current_app.logger.info(f"Verification of inserted document: {verification is not None}")
            else:
                print(f"Verification of inserted document: {verification is not None}")

            return True
        else:
            if hasattr(current_app, 'logger'):
                current_app.logger.warning("MongoDB service not fully initialized, skipping activity logging")
            else:
                print("MongoDB service not fully initialized, skipping activity logging")
            return False
    except Exception as e:
        if hasattr(current_app, 'logger'):
            current_app.logger.error(f"Failed to log user activity: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
        else:
            print(f"Failed to log user activity: {str(e)}")
            import traceback
            print(traceback.format_exc())
        return False

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