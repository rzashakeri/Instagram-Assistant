# encoding: utf-8
import json
import os
import re
import time
from logging import getLogger

import requests
import validators
from file_validator.utils import guess_the_type
from filetype import guess
from instagrapi import Client
from instagrapi.exceptions import ClientError
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import MediaNotFound
from instagrapi.exceptions import PrivateError
from instagrapi.exceptions import UnknownError
from instagrapi.exceptions import UserNotFound
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from configurations import settings
from constants import BACK
from constants import LOGIN
from constants.keys import BACK_KEY
from constants.media_types import ALBUM
from constants.media_types import IGTV
from constants.media_types import PHOTO
from constants.media_types import REEL
from constants.media_types import VIDEO
from constants.messages import DOWNLOAD_COMPLETED
from constants.messages import IS_VIDEO
from constants.messages import LINK_IS_INVALID
from constants.messages import OK_SEND_ME_THE_LINK_YOU_WANT_TO_DOWNLOAD
from constants.messages import STARTING_DOWNLOAD
from constants.messages import UPLOAD_IN_TELEGRAM
from constants.product_types import IS_CLIPS
from constants.product_types import IS_FEED
from constants.product_types import IS_IGTV
from constants.states import DOWNLOAD_STATE
from constants.states import HOME_STATE
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from utils.decorators import send_action

# Init logger
logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def get_media_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    time.sleep(5)
    await update.message.reply_text(
        OK_SEND_ME_THE_LINK_YOU_WANT_TO_DOWNLOAD, reply_markup=back_keyboard
    )
    return DOWNLOAD_STATE


@send_action(ChatAction.UPLOAD_DOCUMENT)
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(
            "what do you want ?", reply_markup=base_keyboard
        )
        return HOME_STATE
    client = Client()
    client.delay_range = [1, 3]
    message_is_url = validators.url(message)
    current_directory = os.getcwd()

    download_directory = f"{current_directory}/download"
    download_directory_is_exist = os.path.exists(download_directory)
    if not download_directory_is_exist:
        os.makedirs(download_directory)

    login_directory = f"{current_directory}/{LOGIN.lower()}"
    login_directory_is_exist = os.path.exists(login_directory)
    if not login_directory_is_exist:
        os.makedirs(login_directory)

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
                    break
                except LoginRequired:
                    if user_instagram_session_is_exist:
                        os.remove(user_instagram_session_path)
                    client.login(user["username"], user["password"])
                    client.dump_settings(user_instagram_session_path)
            client.login(user["username"], user["password"])
            client.dump_settings(
                f"{login_directory}/{user['username']}_{settings.TELEGRAM_USER_ID}.json"
            )
            break
        except (ClientError, PrivateError):
            pass

    if message_is_url:
        try:
            media_pk_from_url = client.media_pk_from_url(message)
            media_info = client.media_info(media_pk_from_url).dict()
        except (MediaNotFound, UnknownError):
            regex = r"(?<=instagram.com\/)[A-Za-z0-9_.]+"
            username = re.findall(regex, message)[0]
            try:
                user_data = client.user_info_by_username(username).dict()
            except UserNotFound:
                await update.message.reply_text(
                    LINK_IS_INVALID,
                    reply_markup=base_keyboard,
                )
                return HOME_STATE
            user_profile_picture_url = user_data["profile_pic_url_hd"]
            request = requests.get(user_profile_picture_url)
            profile_picture_extension = guess(request.content).EXTENSION
            profile_picture_file_name = (
                f"{username}_profile_picture.{profile_picture_extension}"
            )
            profile_picture_file_path = (
                f"{download_directory}/{profile_picture_file_name}"
            )
            with open(profile_picture_file_path, "wb") as file:
                file.write(request.content)
            await update.message.reply_text(
                UPLOAD_IN_TELEGRAM, reply_markup=base_keyboard
            )
            await update.effective_user.send_photo(photo=profile_picture_file_path)
            os.remove(profile_picture_file_path)
            del request
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME_STATE
        media_type = media_info["media_type"]
        product_type = media_info["product_type"]
        if media_type == PHOTO:
            file_path = client.photo_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            await update.message.reply_text(
                UPLOAD_IN_TELEGRAM, reply_markup=base_keyboard
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_photo(photo=file, write_timeout=20)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME_STATE
        elif media_type == VIDEO and product_type == IS_FEED:
            file_path = client.video_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            await update.message.reply_text(
                UPLOAD_IN_TELEGRAM, reply_markup=base_keyboard
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_video(video=file, write_timeout=20)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME_STATE
        elif media_type == IGTV and product_type == IS_IGTV:
            file_path = client.igtv_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            await update.message.reply_text(
                UPLOAD_IN_TELEGRAM, reply_markup=base_keyboard
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_video(video=file, write_timeout=20)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME_STATE
        elif media_type == REEL and product_type == IS_CLIPS:
            file_path = client.clip_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            await update.message.reply_text(
                UPLOAD_IN_TELEGRAM, reply_markup=base_keyboard
            )
            with open(file_path, "rb") as file:
                await update.effective_user.send_video(video=file, write_timeout=20)
            os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME_STATE
        elif media_type == ALBUM:
            files_path = client.album_download(
                media_pk=media_pk_from_url, folder=download_directory
            )
            await update.message.reply_text(
                UPLOAD_IN_TELEGRAM, reply_markup=base_keyboard
            )
            for file_path in files_path:
                with open(file_path, "rb") as file:
                    file_type = guess_the_type(file_path=file_path)
                    if file_type == IS_VIDEO:
                        await update.effective_user.send_video(
                            video=file, write_timeout=20
                        )
                    else:
                        await update.effective_user.send_photo(
                            photo=file, write_timeout=20
                        )
                    os.remove(file_path)
            await update.message.reply_text(
                DOWNLOAD_COMPLETED, reply_markup=base_keyboard
            )
            return HOME_STATE
        else:
            await update.message.reply_text(LINK_IS_INVALID, reply_markup=back_keyboard)
            return HOME_STATE
    elif message.startswith("@"):
        username = message.split("@")[1]
        user_data = client.user_info_by_username(username).dict()
        user_profile_picture_url = user_data["profile_pic_url_hd"]
        request = requests.get(user_profile_picture_url)
        profile_picture_extension = guess(request.content).EXTENSION
        profile_picture_file_name = (
            f"{username}_profile_picture.{profile_picture_extension}"
        )
        profile_picture_file_path = f"{download_directory}/{profile_picture_file_name}"
        with open(profile_picture_file_path, "wb") as file:
            file.write(request.content)
        await update.message.reply_text(UPLOAD_IN_TELEGRAM, reply_markup=base_keyboard)
        await update.effective_user.send_photo(photo=profile_picture_file_path)
        os.remove(profile_picture_file_path)
        del request
        await update.message.reply_text(DOWNLOAD_COMPLETED, reply_markup=base_keyboard)
        return HOME_STATE
    else:
        await update.message.reply_text(LINK_IS_INVALID, reply_markup=back_keyboard)
