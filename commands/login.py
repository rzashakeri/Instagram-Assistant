# encoding: utf-8
import os
from logging import getLogger

from instagrapi import Client
from telegram import Update
from telegram.ext import ContextTypes

from core.constants import HOME, BACK_TO_HOME, BACK, LOGIN, LOGIN_TO_INSTAGRAM
from core.keyboards import base_keyboard, back_keyboard

# Init logger
logger = getLogger(__name__)


async def get_login_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    message_for_get_login_data: str = (
        "Please send me login information in the following format and format: \n"
        "\n"
        "username\n"
        "password"
    )
    await update.message.reply_text(
        message_for_get_login_data, reply_markup=back_keyboard
    )
    return LOGIN_TO_INSTAGRAM


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    user_id = update.effective_user.id
    if message == BACK:
        await update.message.reply_text(
            "what do you want ?", reply_markup=base_keyboard
        )
        return HOME
    username, password = message.split("\n")
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/login"
    login_directory_is_exist = os.path.isdir(login_directory)
    if not login_directory_is_exist:
        os.makedirs(login_directory)
    client = Client()
    client.set_proxy("socks5://127.0.0.1:30235")
    user_instagram_session = f"{login_directory}/{username}_{user_id}.json"
    user_instagram_session_is_exist = os.path.exists(user_instagram_session)
    if user_instagram_session_is_exist:
        client.load_settings(user_instagram_session)
        client.login(username, password)
        client.get_timeline_feed()
        await update.effective_user.send_message(
            "You Were Already Logged In", reply_markup=base_keyboard
        )
        return HOME
    client.login(username, password)
    client.dump_settings(f"{login_directory}/{username}_{user_id}.json")
    await update.effective_user.send_message(
        "Logged In Successfully", reply_markup=base_keyboard
    )
    return HOME
