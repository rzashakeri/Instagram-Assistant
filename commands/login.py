# encoding: utf-8
import os
from logging import getLogger

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
from telegram import Update
from telegram.ext import ContextTypes

from constants import BACK, LOGIN
from constants.messages import MESSAGE_FOR_GET_LOGIN_DATA, WHAT_DO_YOU_WANT, YOU_WERE_ALREADY_LOGGED_IN, LOGGED_IN_SUCCESSFULLY
from constants.states import LOGIN_STATE, HOME_STATE
from core.keyboards import base_keyboard, back_keyboard

# Init logger
logger = getLogger(__name__)


async def get_login_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    message_for_get_login_data: str = MESSAGE_FOR_GET_LOGIN_DATA
    await update.message.reply_text(
        message_for_get_login_data, reply_markup=back_keyboard
    )
    return LOGIN_STATE


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message == BACK:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    username, password = message.split("\n")
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    user_instagram_session = f"{login_directory}/{username}_{user_id}.json"
    login_directory_is_exist = os.path.isdir(login_directory)
    user_instagram_session_is_exist = os.path.exists(user_instagram_session)
    if not login_directory_is_exist:
        os.makedirs(login_directory)
    client = Client()
    if user_instagram_session_is_exist:
        client.load_settings(user_instagram_session)
        client.login(username, password)
        try:
            client.get_timeline_feed()
        except LoginRequired:
            os.remove(user_instagram_session)
            client.login(username, password)
            client.dump_settings(f"{login_directory}/{username}_{user_id}.json")
        except ClientError as error:
            if "Please wait a few minutes before you try again" in error.message:
                await update.effective_user.send_message(
                    "Please wait a few minutes before you try again", reply_markup=base_keyboard
                )
                return HOME_STATE
        await update.effective_user.send_message(
            YOU_WERE_ALREADY_LOGGED_IN, reply_markup=base_keyboard
        )
        return HOME_STATE
    client.login(username, password)
    client.dump_settings(f"{login_directory}/{username}_{user_id}.json")
    await update.effective_user.send_message(
        LOGGED_IN_SUCCESSFULLY, reply_markup=base_keyboard
    )
    return HOME_STATE
