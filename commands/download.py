# encoding: utf-8
import os
import re
import shutil

import requests
from logging import getLogger

from filetype import guess
from instagrapi import Client
from instagrapi.exceptions import MediaNotFound, UnknownError
from telegram import Update
from telegram.ext import ContextTypes
from file_validator.utils import guess_the_type
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
    VIDEO,
    IS_FEED,
    IS_IGTV,
    IS_CLIPS,
    DOWNLOAD_COMPLETED,
    ALBUM,
    IGTV,
    REEL,
    IS_VIDEO,
)
from core.keyboards import base_keyboard, back_keyboard

# Init logger
logger = getLogger(__name__)


async def get_media_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    welcome_message: str = "OK, send me the link you want to download from Instagram Such Profile, Post, Story and etc..."
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
    user_instagram_session = f"{login_directory}/{settings.INSTAGRAM_USERNAME}_{settings.TELEGRAM_USER_ID}.json"
    login_directory_is_exist = os.path.exists(login_directory)
    download_directory_is_exist = os.path.exists(download_directory)
    user_instagram_session_is_exist = os.path.exists(user_instagram_session)
    message_is_url = validators.url(message)
    client = Client()
    if not login_directory_is_exist:
        os.makedirs(login_directory)
    if not download_directory_is_exist:
        os.makedirs(download_directory)
    if message_is_url:
        if user_instagram_session_is_exist:
            client.load_settings(user_instagram_session)
            client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
            client.get_timeline_feed()
        client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
        client.dump_settings(
            f"{login_directory}/{settings.INSTAGRAM_USERNAME}_{settings.TELEGRAM_USER_ID}.json"
        )
        try:
            media_pk_from_url = client.media_pk_from_url(message)
            media_info = client.media_info(media_pk_from_url).dict()
        except (MediaNotFound, UnknownError):
            regex = r"(?<=instagram.com\/)[A-Za-z0-9_.]+"
            username = re.findall(regex, message)[0]
            user_data = client.user_info_by_username(username).dict()
            user_profile_picture_url = user_data["profile_pic_url_hd"]
            request = requests.get(user_profile_picture_url)
            profile_picture_extension = guess(request.content).EXTENSION
            profile_picture_file_name = f"{username}_profile_picture.{profile_picture_extension}"
            profile_picture_file_path = f"{download_directory}/{profile_picture_file_name}"
            with open(profile_picture_file_path, "wb") as file:
                file.write(request.content)
            await update.effective_user.send_photo(photo=profile_picture_file_path)
            os.remove(profile_picture_file_path)
            del request
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME
        media_type = media_info["media_type"]
        product_type = media_info["product_type"]
        if media_type == PHOTO:
            file_path = client.photo_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_photo(photo=file)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME
        if media_type == VIDEO and product_type == IS_FEED:
            file_path = client.video_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_video(video=file)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME
        if media_type == IGTV and product_type == IS_IGTV:
            file_path = client.igtv_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_video(video=file)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME
        if media_type == REEL and product_type == IS_CLIPS:
            file_path = client.clip_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_video(video=file)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME
        if media_type == ALBUM:
            files_path = client.album_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            for file_path in files_path:
                with open(file_path, "rb") as file:
                    file_type = guess_the_type(file_path=file_path)
                    if file_type == IS_VIDEO:
                        await update.effective_user.send_video(video=file)
                    else:
                        await update.effective_user.send_photo(photo=file)
                    os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME
