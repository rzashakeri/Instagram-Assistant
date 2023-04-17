# encoding: utf-8
import json
import os
import time
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
from constants import BACK, YES
from constants import LOGIN
from constants.keys import BACK_KEY
from constants.messages import LOGGED_IN_SUCCESSFULLY, REMEMBER_ME
from constants.messages import MESSAGE_FOR_GET_LOGIN_DATA
from constants.messages import PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN
from constants.messages import SOMETHING_WENT_WRONG
from constants.messages import WHAT_DO_YOU_WANT
from constants.messages import YOU_WERE_ALREADY_LOGGED_IN
from constants.states import (
    HOME_STATE,
    IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN,
    LOGIN_WITH_TWO_FACTOR_AUTHENTICATION,
)
from constants.states import LOGIN_STATE
from core.keyboards import back_keyboard, yes_or_no_keyboard
from core.keyboards import base_keyboard
from utils.decorators import send_action

# Init logger
logger = getLogger(__name__)

CLIENT = Client()
CLIENT.delay_range = [1, 3]
SAVED_LOGIN_INFORMATION = None
USERNAME = None
PASSWORD = None


@send_action(ChatAction.TYPING)
async def get_login_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    logger.info("get login information")
    await update.message.reply_text(
        MESSAGE_FOR_GET_LOGIN_DATA, reply_markup=back_keyboard
    )
    return IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN


@send_action(ChatAction.TYPING)
async def remember_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    logger.info("Is your login information saved for the next login?")
    message = update.message.text
    try:
        global USERNAME
        global PASSWORD
        USERNAME, PASSWORD = message.split("\n")
    except ValueError:
        await update.message.reply_text(
            MESSAGE_FOR_GET_LOGIN_DATA, reply_markup=back_keyboard
        )
        return IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN
    await update.message.reply_text(
        "⚠️ Attention: This robot saves a session for next Login if you want",
        reply_markup=back_keyboard,
    )
    await update.message.reply_text(REMEMBER_ME, reply_markup=yes_or_no_keyboard)
    return LOGIN_STATE


@send_action(ChatAction.TYPING)
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    logger.info("login attempt")
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    user_instagram_session = f"{login_directory}/{USERNAME}_{user_id}.json"
    user_instagram_session_is_exist = os.path.exists(user_instagram_session)
    if user_instagram_session_is_exist:
        CLIENT.load_settings(user_instagram_session)
        CLIENT.login(USERNAME, PASSWORD)
        try:
            CLIENT.get_timeline_feed()
        except LoginRequired:
            os.remove(user_instagram_session)
            CLIENT.login(USERNAME, PASSWORD)
            CLIENT.dump_settings(f"{login_directory}/{USERNAME}_{user_id}.json")
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
    global SAVED_LOGIN_INFORMATION
    try:
        if message == YES:
            logger.info("Saved login information for %s", USERNAME)
            SAVED_LOGIN_INFORMATION = True
            CLIENT.login(USERNAME, PASSWORD)
            CLIENT.dump_settings(f"{login_directory}/{USERNAME}_{user_id}.json")
        else:
            logger.info("not Save login information for %s", USERNAME)
            SAVED_LOGIN_INFORMATION = False
            CLIENT.login(USERNAME, PASSWORD)
        await update.effective_user.send_message(
            LOGGED_IN_SUCCESSFULLY, reply_markup=base_keyboard
        )
        return HOME_STATE
    except TwoFactorRequired:
        logger.info("Get Two Factor Authentication Code")
        await update.effective_user.send_message(
            "Please Send Two Factor Authentication Code", reply_markup=back_keyboard
        )
        return LOGIN_WITH_TWO_FACTOR_AUTHENTICATION
    except ClientForbiddenError:
        await update.effective_user.send_message(
            SOMETHING_WENT_WRONG,
            reply_markup=base_keyboard,
        )
        return HOME_STATE


@send_action(ChatAction.TYPING)
async def login_with_two_factor_authentication(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    logger.info("Login With Two Factor Authentication Code")
    time.sleep(5)
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    verification_code = message
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    global SAVED_LOGIN_INFORMATION
    if SAVED_LOGIN_INFORMATION:
        CLIENT.login(
            username=USERNAME, password=PASSWORD, verification_code=verification_code
        )
        CLIENT.dump_settings(f"{login_directory}/{USERNAME}_{user_id}.json")
        await update.effective_user.send_message(
            LOGGED_IN_SUCCESSFULLY, reply_markup=base_keyboard
        )
        return HOME_STATE
    CLIENT.login(
        username=USERNAME, password=PASSWORD, verification_code=verification_code
    )
    await update.effective_user.send_message(
        LOGGED_IN_SUCCESSFULLY, reply_markup=base_keyboard
    )
    return HOME_STATE


def login_admin_user_to_instagram(client):
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
