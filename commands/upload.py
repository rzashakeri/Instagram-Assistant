# encoding: utf-8
import os
from logging import getLogger

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
from telegram import Update
from telegram.ext import ContextTypes

from constants import BACK, LOGIN
from constants.messages import MESSAGE_FOR_GET_LOGIN_DATA, WHAT_DO_YOU_WANT, YOU_WERE_ALREADY_LOGGED_IN, LOGGED_IN_SUCCESSFULLY, SEND_ME_THE_FILE_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM, SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM
from constants.states import LOGIN_STATE, HOME_STATE, UPLOAD_STATE, LOGIN_TO_INSTAGRAM_FOR_UPLOAD_MEDIA_STATE, GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE, GET_CAPTION_OF_POST_FOR_UPLOAD_IN_INSTAGRAM_STATE
from core.keyboards import base_keyboard, back_keyboard

file = None
caption = None


async def get_login_data_for_upload_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message == BACK:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    message_for_get_login_data: str = MESSAGE_FOR_GET_LOGIN_DATA
    await update.message.reply_text(
        message_for_get_login_data, reply_markup=back_keyboard
    )
    return LOGIN_TO_INSTAGRAM_FOR_UPLOAD_MEDIA_STATE


async def login_to_instagram_for_upload_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
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
            await update.effective_user.send_message(
                SEND_ME_THE_FILE_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM, reply_markup=back_keyboard
            )
            return GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE
        except LoginRequired:
            os.remove(user_instagram_session)
            client.login(username, password)
            client.dump_settings(f"{login_directory}/{username}_{user_id}.json")
            await update.effective_user.send_message(
                SEND_ME_THE_FILE_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM, reply_markup=back_keyboard
            )
            return GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE
        except ClientError as error:
            if "Please wait a few minutes before you try again" in error.message:
                await update.effective_user.send_message(
                    "Please wait a few minutes before you try again", reply_markup=base_keyboard
                )
                return HOME_STATE
    client.login(username, password)
    client.dump_settings(f"{login_directory}/{username}_{user_id}.json")
    await update.effective_user.send_message(
        SEND_ME_THE_FILE_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM, reply_markup=back_keyboard
    )
    return GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE

async def get_file_for_upload_in_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    message = update.message
    if message.text == BACK:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    global file
    file_url = context.bot.get_file(update.message.document.file_id).get_file_url()
    await update.effective_user.send_message(
        file_url, reply_markup=back_keyboard
    )
    return GET_CAPTION_OF_POST_FOR_UPLOAD_IN_INSTAGRAM_STATE


async def get_caption_of_post_for_upload_in_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message == BACK:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    global caption
    caption = update.message.text
    await update.effective_user.send_message(
        SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM, reply_markup=back_keyboard
    )
    return GET_CAPTION_OF_POST_FOR_UPLOAD_IN_INSTAGRAM_STATE
