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
    if message == BACK:
        await update.message.reply_text(
            "what do you want ?", reply_markup=base_keyboard
        )
        return HOME
    current_directory = os.getcwd()
    login_directory = f'{current_directory}/login'
    login_directory_is_exist = os.path.isdir(login_directory)
    if not login_directory_is_exist:
        os.makedirs(login_directory)
    username, password = message.split('\n')
    client = Client()
    instagram_session = client.load_settings(f'{login_directory}/{username}.json')
    if instagram_session is not None:
        client.login(username, password)
        client.get_timeline_feed()
        await update.effective_user.send_message('You Were Already Logged In')
    else:
        client.login(username, password)
        client.dump_settings(f'{login_directory}/{username}.json')
        await update.effective_user.send_message('Logged In Successfully')

    return HOME
