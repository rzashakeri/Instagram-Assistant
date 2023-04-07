# encoding: utf-8
import os
from logging import getLogger

import validators
from instagrapi import Client
from instagrapi.exceptions import ClientError
from instagrapi.exceptions import LoginRequired
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from configurations import settings
from constants import BACK
from constants import LOGIN
from constants.keys import BACK_KEY
from constants.messages import INSIGHT_OF_MEDIA
from constants.messages import LINK_IS_INVALID
from constants.messages import PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN
from constants.messages import SEND_THE_POST_LINK_YOU_WANT_TO_GET_THE_STATISTICS
from constants.states import HOME_STATE
from constants.states import INSIGHT_STATE
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from utils.decorators import send_action
# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def get_media_link(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        SEND_THE_POST_LINK_YOU_WANT_TO_GET_THE_STATISTICS,
        reply_markup=back_keyboard,
    )
    return INSIGHT_STATE


@send_action(ChatAction.TYPING)
async def insight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text("what do you want ?",
                                        reply_markup=base_keyboard)
        return HOME_STATE
    current_directory = os.getcwd()
    download_directory = f"{current_directory}/download"
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    user_instagram_session_name = (
        f"{settings.INSTAGRAM_USERNAME}_{settings.TELEGRAM_USER_ID}.json")
    user_instagram_session_path = f"{login_directory}/{user_instagram_session_name}"
    login_directory_is_exist = os.path.exists(login_directory)
    download_directory_is_exist = os.path.exists(download_directory)
    user_instagram_session_is_exist = os.path.exists(
        user_instagram_session_path)
    client = Client()
    if not login_directory_is_exist:
        os.makedirs(login_directory)
    if not download_directory_is_exist:
        os.makedirs(download_directory)
    message_is_url = validators.url(message)
    if message_is_url:
        if user_instagram_session_is_exist:
            client.load_settings(user_instagram_session_path)
            client.login(settings.INSTAGRAM_USERNAME,
                         settings.INSTAGRAM_PASSWORD)
            try:
                client.get_timeline_feed()
            except LoginRequired:
                if user_instagram_session_is_exist:
                    os.remove(user_instagram_session_path)
                client.login(settings.INSTAGRAM_USERNAME,
                             settings.INSTAGRAM_PASSWORD)
                client.dump_settings(user_instagram_session_path)
            except ClientError as error:
                if PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN in error.message:
                    await update.effective_user.send_message(
                        PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN,
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
        client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
        client.dump_settings(
            f"{login_directory}/{settings.INSTAGRAM_USERNAME}_{settings.TELEGRAM_USER_ID}.json"
        )
        media_pk_from_url = client.media_pk_from_url(message)
        insight_of_media = client.insights_media(media_pk_from_url)
        comment_count = insight_of_media.get("comment_count")
        like_count = insight_of_media.get("like_count")
        save_count = insight_of_media.get("save_count")
        await update.effective_user.send_message(
            INSIGHT_OF_MEDIA.format(
                comment_count=comment_count,
                like_count=like_count,
                save_count=save_count,
            ),
            reply_markup=base_keyboard,
        )
        return HOME_STATE
    else:
        await update.message.reply_text(LINK_IS_INVALID,
                                        reply_markup=back_keyboard)
