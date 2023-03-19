# encoding: utf-8
import os
from logging import getLogger

from instagrapi import Client
from telegram import Update
from telegram.ext import ContextTypes
import validators

from configurations import settings
from core.constants import (
    HOME,
    BACK,
    DOWNLOAD_MEDIA,
    YOU_WERE_ALREADY_LOGGED_IN,
    LOGIN,
    LOGGED_IN_SUCCESSFULLY,
    PHOTO,
)
from core.keyboards import base_keyboard, back_keyboard

# Init logger
logger = getLogger(__name__)


async def get_media_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    welcome_message: str = "OK, send me the link you want to download from Instagram"
    await update.message.reply_text(welcome_message, reply_markup=back_keyboard)
    return DOWNLOAD_MEDIA


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    message = update.message.text
    if message == BACK:
        await update.message.reply_text(
            "what do you want ?", reply_markup=base_keyboard
        )
        return HOME
    current_directory = os.getcwd()
    download_directory = f"{current_directory}/download"
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    user_instagram_session = (
        f"{login_directory}/{settings.INSTAGRAM_USERNAME}_{settings.TELEGRAM_USER_ID}.json"
    )
    login_directory_is_exist = os.path.exists(login_directory)
    download_directory_is_exist = os.path.exists(download_directory)
    user_instagram_session_is_exist = os.path.exists(user_instagram_session)
    message_is_link = validators.email(message)
    client = Client()
    if not login_directory_is_exist:
        os.makedirs(login_directory)
    if not download_directory_is_exist:
        os.makedirs(download_directory)
    if message_is_link:
        if user_instagram_session_is_exist:
            client.load_settings(user_instagram_session)
            client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
            client.get_timeline_feed()
        client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
        client.dump_settings(
            f"{login_directory}/{settings.INSTAGRAM_USERNAME}_{settings.TELEGRAM_USER_ID}.json"
        )
        media_pk_from_url = client.media_pk_from_url(message)
        media_info = client.media_info(media_pk_from_url).dict()
        media_type = media_info["media_type"]
        product_type = media_info["product_type"]
        if media_type == PHOTO:
            file_path = client.photo_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            with open(file_path, 'rb') as file:
                await update.effective_user.send_photo(photo=file)
