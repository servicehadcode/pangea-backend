from flask import Blueprint, redirect, request, session, jsonify, current_app
from utils.github_oauth import get_access_token, get_user_info
from services.mongo_service import mongo_service
from models.user_activity_model import create_user_activity
from services.activity_service import log_user_activity


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login/github")
def login_github():
    redirect_url = request.args.get("redirect", current_app.config["FRONTEND_URL"])
    session["redirect_after_login"] = redirect_url

    github_oauth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={current_app.config['GITHUB_CLIENT_ID']}&scope=user:email"
    )
    return redirect(github_oauth_url)


@auth_bp.route("/login/github/callback")
def github_callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    token = get_access_token(code)
    if not token:
        return "Failed to get access token", 400

    user_info = get_user_info(token)

    # Fallback email logic
    username = user_info.get("login")
    email = user_info.get("email") or f"{username}@users.noreply.github.com"

    if not username:
        current_app.logger.error("GitHub user info missing username")
        return "GitHub login failed", 400

    session["user"] = {
        "username": username,
        "email": email,
        "name": user_info.get("name"),
        "avatar": user_info.get("avatar_url")
    }
    session.modified = True

    current_app.logger.info(f"User info stored in session: {session['user']}")
    mongo_service.user_activity.insert_one(create_user_activity(user_info, "signin"))

    return redirect(session.pop("redirect_after_login", current_app.config["FRONTEND_URL"]))



@auth_bp.route("/me")
def get_me():
    if "user" not in session:
        current_app.logger.info("Session does not contain user")
        return jsonify({}), 401
    return jsonify(session["user"])

@auth_bp.route("/logout", methods=["POST"])
def logout():
    user_data = session.get("user")
    if user_data:
        log_user_activity(user_data, "logout")
    session.clear()
    return jsonify({"message": "Logged out"}), 200

