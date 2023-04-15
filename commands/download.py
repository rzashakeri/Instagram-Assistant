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

from commands.login import login_admin_user_to_instagram
from configurations import settings
from constants import BACK
from constants import LOGIN
from constants import PROCESSING
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
from constants.messages import SOMETHING_WENT_WRONG
from constants.messages import STARTING_DOWNLOAD
from constants.messages import UPLOAD_IN_TELEGRAM
from constants.messages import USER_NOT_FOUND_CHECK_USERNAME_AND_TRY_AGAIN
from constants.product_types import IS_CLIPS
from constants.product_types import IS_FEED
from constants.product_types import IS_IGTV
from constants.states import DOWNLOAD_STATE
from constants.states import HOME_STATE
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from utils import create_requirement_folders
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


@send_action(ChatAction.TYPING)
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
    logged_in_user = login_admin_user_to_instagram(client)
    if not logged_in_user:
        await update.message.reply_text(
            SOMETHING_WENT_WRONG, reply_markup=base_keyboard
        )
        return HOME_STATE

    if message_is_url:
        try:
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
            )
            processing_message = await context.bot.send_message(
                chat_id=update.message.chat_id, text=PROCESSING
            )
            media_pk_from_url = client.media_pk_from_url(message)
            media_info = client.media_info(media_pk_from_url).dict()
            await context.bot.deleteMessage(
                message_id=processing_message.message_id, chat_id=update.message.chat_id
            )
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
            await update.effective_user.send_photo(
                photo=user_profile_picture_url, reply_markup=base_keyboard
            )
            return HOME_STATE
        media_type = media_info["media_type"]
        product_type = media_info["product_type"]
        if media_type == PHOTO:
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO
            )
            await update.effective_user.send_photo(
                photo=media_info["thumbnail_url"],
                caption=media_info["caption_text"],
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        elif (
            media_type == VIDEO
            and product_type == IS_FEED
            or media_type == IGTV
            and product_type == IS_IGTV
            or media_type == REEL
            and product_type == IS_CLIPS
        ):
            await update.effective_user.send_video(
                video=media_info["video_url"],
                caption=media_info["caption_text"],
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        elif media_type == ALBUM:
            for media in media_info["resources"]:
                if media["video_url"] is not None:
                    await update.effective_user.send_video(video=media["video_url"])
                else:
                    await update.effective_user.send_photo(photo=media["thumbnail_url"])
            await update.effective_user.send_message(
                text=media_info["caption_text"], reply_markup=base_keyboard
            )
            return HOME_STATE
        else:
            await update.message.reply_text(LINK_IS_INVALID, reply_markup=back_keyboard)
            return HOME_STATE
    elif message.startswith("@"):
        username = message.split("@")[1]
        try:
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
            )
            processing_message = await context.bot.send_message(
                chat_id=update.message.chat_id, text=PROCESSING
            )
            user_data = client.user_info_by_username(username).dict()
            await context.bot.deleteMessage(
                message_id=processing_message.message_id, chat_id=update.message.chat_id
            )
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO
            )
            user_profile_picture_url = user_data["profile_pic_url_hd"]
            await update.effective_user.send_photo(
                photo=user_profile_picture_url, reply_markup=base_keyboard
            )
            return HOME_STATE
        except UserNotFound:
            await context.bot.deleteMessage(
                message_id=processing_message.message_id, chat_id=update.message.chat_id
            )
            await update.message.reply_text(
                USER_NOT_FOUND_CHECK_USERNAME_AND_TRY_AGAIN, reply_markup=back_keyboard
            )
    else:
        await update.message.reply_text(LINK_IS_INVALID, reply_markup=base_keyboard)
