# encoding: utf-8
import json
import os
from logging import getLogger

from configurations import settings
from constants import LOGIN
from core.exceptions import LoginException
from core.instagram import CustomClient

# Init logger
logger = getLogger(__name__)

CLIENT = None
USERNAME = None
PASSWORD = None
SAVED_LOGIN_INFORMATION = None


def login_admin_user_to_instagram():
    """login user"""
    logger.info("Login Admin User")
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    with open("admin_users.json", encoding="utf-8") as file:
        users = json.load(file)
    for user in users["users"]:
        user_instagram_session_name = (
            f"{user['username']}_{settings.ADMIN_TELEGRAM_USER_ID}.json")
        user_instagram_session_path = f"{login_directory}/{user_instagram_session_name}"
        try:
            client = CustomClient(username=USERNAME, password=USERNAME).get_client(
                login_directory=login_directory,
                telegram_user_id=settings.ADMIN_TELEGRAM_USER_ID,
                user_instagram_session=user_instagram_session_path,
                save_session=True,
            )
            return client
        except LoginException:
            pass
