# encoding: utf-8
import os
from logging import getLogger

import validators
from instagrapi import Client
from instagrapi.exceptions import ClientError
from instagrapi.exceptions import LoginRequired
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
from constants.messages import GETTING_MEDIA_INFORMATION
from constants.messages import GETTING_PROFILE_INFORMATION
from constants.messages import INSIGHT_OF_MEDIA
from constants.messages import LINK_IS_INVALID
from constants.messages import PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN
from constants.messages import SEND_THE_POST_LINK_YOU_WANT_TO_GET_THE_STATISTICS
from constants.messages import SOMETHING_WENT_WRONG
from constants.messages import USER_INFO
from constants.messages import USER_NOT_FOUND_CHECK_USERNAME_AND_TRY_AGAIN
from constants.messages import WHAT_DO_YOU_WANT
from constants.states import HOME_STATE
from constants.states import INSIGHT_STATE
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
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    client = Client()
    client.delay_range = [1, 3]
    message_is_url = validators.url(message)
    await context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
    )
    bot_message = await context.bot.send_message(
        chat_id=update.message.chat_id, text=PROCESSING
    )
    logged_in_user = login_admin_user_to_instagram(client)
    if not logged_in_user:
        await context.bot.editMessageText(
            chat_id=update.message.chat_id,
            message_id=bot_message.message_id,
            text=SOMETHING_WENT_WRONG,
        )
        return HOME_STATE

    if message_is_url:
        await context.bot.editMessageText(
            chat_id=update.message.chat_id,
            message_id=bot_message.message_id,
            text=GETTING_MEDIA_INFORMATION,
        )
        media_pk_from_url = client.media_pk_from_url(message)
        insight_of_media = client.insights_media(media_pk_from_url)
        comment_count = insight_of_media.get("comment_count")
        like_count = insight_of_media.get("like_count")
        save_count = insight_of_media.get("save_count")
        share_count = insight_of_media.get("reshare_count")
        await context.bot.deleteMessage(
            message_id=bot_message.message_id,
            chat_id=update.message.chat_id,
        )
        await update.effective_user.send_message(
            INSIGHT_OF_MEDIA.format(
                comment_count=comment_count,
                like_count=like_count,
                save_count=save_count,
                share_count=share_count,
            ),
            reply_markup=base_keyboard,
        )
        return HOME_STATE
    elif message.startswith("@"):
        username = message.split("@")[1]
        await context.bot.editMessageText(
            chat_id=update.message.chat_id,
            message_id=bot_message.message_id,
            text=GETTING_PROFILE_INFORMATION,
        )
        try:
            user_info = client.user_info_by_username(username).dict()
            full_name = user_info["full_name"]
            following = user_info["following_count"]
            follower = user_info["follower_count"]
            media_count = user_info["media_count"]
            biography = user_info["biography"]
            user_profile_picture_url = user_info["profile_pic_url_hd"]
            await context.bot.deleteMessage(
                message_id=bot_message.message_id,
                chat_id=update.message.chat_id,
            )
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO
            )
            await update.effective_user.send_photo(
                photo=user_profile_picture_url,
                reply_markup=base_keyboard,
                caption=USER_INFO.format(
                    username=username,
                    full_name=full_name,
                    following=following,
                    follower=follower,
                    media_count=media_count,
                    biography=biography,
                ),
            )
            return HOME_STATE
        except UserNotFound:
            await context.bot.deleteMessage(
                message_id=bot_message.message_id, chat_id=update.message.chat_id
            )
            await update.message.reply_text(
                USER_NOT_FOUND_CHECK_USERNAME_AND_TRY_AGAIN, reply_markup=back_keyboard
            )

    else:
        await update.message.reply_text(LINK_IS_INVALID, reply_markup=back_keyboard)
