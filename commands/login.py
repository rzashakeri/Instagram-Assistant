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
    current_directory = os.getcwd()
    if message == BACK:
        await update.message.reply_text(
            "what do you want ?", reply_markup=base_keyboard
        )
        return HOME
    username, password = message.split('\n')
    client = Client()
    client.login(username, password)
    client.dump_settings(f'{current_directory}/tmp/{username}.json')
    await update.effective_user.send_message('login success')

    return HOME
