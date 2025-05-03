from datetime import datetime, timezone

def create_user_activity(user_info, action):
    # Handle both GitHub API response format and our internal user format
    username = user_info.get("login") or user_info.get("username")
    email = user_info.get("email") or f"{username}@users.noreply.github.com" if username else None

    return {
        "username": username,
        "email": email,
        "action": action,
        "timestamp": datetime.now(timezone.utc)
    }
