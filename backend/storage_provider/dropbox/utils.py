import json
import time
from typing import Dict

import httpx

from backend.config import Config


def refresh_dropbox_token(refresh_token):
    """Refresh Dropbox access token using stored refresh token"""
    token_url = "https://api.dropboxapi.com/oauth2/token"
    data = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_id": Config.DROPBOX_APP_KEY,
        "client_secret": Config.DROPBOX_APP_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = httpx.post(token_url, data=data, headers=headers)
    return response.json()


def get_valid_dropbox_token(credentials: Dict):
    """Check if Dropbox token is expired and refresh if needed"""

    if int(time.time()) > credentials["expires_in"]:
        new_token_data = refresh_dropbox_token(credentials["refresh_token"])
        credentials["access_token"] = new_token_data["access_token"]
        credentials["expires_in"] = int(time.time()) + new_token_data["expires_in"]

    return credentials["access_token"]
