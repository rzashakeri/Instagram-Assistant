# encoding: utf-8
import json
import os
from logging import getLogger

from instagrapi import Client
from instagrapi.exceptions import ClientError
from instagrapi.exceptions import ClientForbiddenError
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import PrivateError
from instagrapi.exceptions import TwoFactorRequired
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from configurations import settings
from constants import BACK
from constants import LOGIN
from constants.keys import BACK_KEY
from constants.messages import LOGGED_IN_SUCCESSFULLY
from constants.messages import MESSAGE_FOR_GET_LOGIN_DATA
from constants.messages import PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN
from constants.messages import SOMETHING_WENT_WRONG
from constants.messages import WHAT_DO_YOU_WANT
from constants.messages import YOU_WERE_ALREADY_LOGGED_IN
from constants.states import HOME_STATE
from constants.states import LOGIN_STATE
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def get_login_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    message_for_get_login_data: str = MESSAGE_FOR_GET_LOGIN_DATA
    await update.message.reply_text(
        message_for_get_login_data, reply_markup=back_keyboard
    )
    return LOGIN_STATE


@send_action(ChatAction.TYPING)
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message == BACK_KEY:
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
    client.delay_range = [1, 3]
    if user_instagram_session_is_exist:
        client.load_settings(user_instagram_session)
        client.login(username, password)
        try:
            client.get_timeline_feed()
        except LoginRequired:
            os.remove(user_instagram_session)
            client.login(username, password)
            client.dump_settings(f"{login_directory}/{username}_{user_id}.json")
        except ClientForbiddenError:
            await update.effective_user.send_message(
                SOMETHING_WENT_WRONG,
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        except ClientError as error:
            if PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN in error.message:
                await update.effective_user.send_message(
                    PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN,
                    reply_markup=base_keyboard,
                )
                return HOME_STATE
        await update.effective_user.send_message(
            YOU_WERE_ALREADY_LOGGED_IN, reply_markup=base_keyboard
        )
        return HOME_STATE
    try:
        client.login(username, password)
        client.dump_settings(f"{login_directory}/{username}_{user_id}.json")
        await update.effective_user.send_message(
            LOGGED_IN_SUCCESSFULLY, reply_markup=base_keyboard
        )
        return HOME_STATE
    except TwoFactorRequired:
        await update.effective_user.send_message(
            "Two-factor authentication required", reply_markup=base_keyboard
        )
        return HOME_STATE
    except ClientForbiddenError:
        await update.effective_user.send_message(
            SOMETHING_WENT_WRONG,
            reply_markup=base_keyboard,
        )
        return HOME_STATE


def login_user(client):
    """login user"""
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    with open("users.json", encoding="utf-8") as file:
        users = json.load(file)
    for user in users["users"]:
        user_instagram_session_name = (
            f"{user['username']}_{settings.TELEGRAM_USER_ID}.json"
        )
        user_instagram_session_path = f"{login_directory}/{user_instagram_session_name}"
        user_instagram_session_is_exist = os.path.exists(user_instagram_session_path)
        try:
            if user_instagram_session_is_exist:
                client.load_settings(user_instagram_session_path)
                client.login(user["username"], user["password"])
                try:
                    client.get_timeline_feed()
                    return True
                except LoginRequired:
                    if user_instagram_session_is_exist:
                        os.remove(user_instagram_session_path)
                    client.login(user["username"], user["password"])
                    client.dump_settings(user_instagram_session_path)
            client.login(user["username"], user["password"])
            client.dump_settings(
                f"{login_directory}/{user['username']}_{settings.TELEGRAM_USER_ID}.json"
            )
            return True
        except (ClientError, PrivateError):
            pass
    return False
