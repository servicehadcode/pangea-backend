from datetime import datetime

def create_user_activity(user_info, action):
    return {
        "username": user_info.get("login"),
        "email": user_info.get("email"),
        "action": action,
        "timestamp": datetime.utcnow()
    }
