# /app/src/utils/github_oauth.py

import requests
from flask import current_app
from dotenv import load_dotenv
import os

load_dotenv()  # To load environment variables from a .env file

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")

def get_access_token(code: str) -> str:
    """Exchange the GitHub OAuth code for an access token."""
    url = "https://github.com/login/oauth/access_token"
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI
    }
    headers = {"Accept": "application/json"}
    response = requests.post(url, data=data, headers=headers)
    current_app.logger.info(f"Making request to GitHub API with data: {data}")

    
    # Log the response for debugging
    current_app.logger.info(f"GitHub access token response: {response.json()}")
    
    response_data = response.json()
    return response_data.get("access_token")

def get_user_info(access_token: str) -> dict:
    """Fetch user information from GitHub using the access token."""
    url = "https://api.github.com/user"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    # Log the full response for debugging
    current_app.logger.info(f"GitHub user info response: {response.json()}")
    
    return response.json()
