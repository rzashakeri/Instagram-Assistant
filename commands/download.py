# encoding: utf-8
import re
import time
from logging import getLogger

import validators
from instagrapi import Client
from instagrapi.exceptions import MediaNotFound
from instagrapi.exceptions import UnknownError
from instagrapi.exceptions import UserNotFound
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from commands.login import login_admin_user_to_instagram
from constants import P_SEGMENT
from constants import PROCESSING
from constants import REEL_SEGMENT
from constants import STORIES_SEGMENT
from constants.keys import BACK_KEY
from constants.media_types import ALBUM
from constants.media_types import IGTV
from constants.media_types import PHOTO
from constants.media_types import REEL
from constants.media_types import STORY
from constants.media_types import VIDEO
from constants.messages import GETTING_MEDIA_INFORMATION
from constants.messages import GETTING_PROFILE_INFORMATION
from constants.messages import GETTING_STORY_INFORMATION
from constants.messages import INSTAGRAM_COM
from constants.messages import LINK_IS_INVALID
from constants.messages import MEDIA_NOT_FOUND
from constants.messages import OK_SEND_ME_THE_LINK_YOU_WANT_TO_DOWNLOAD
from constants.messages import PLEASE_SEND_THE_INSTAGRAM_LINK
from constants.messages import SENDING_THUMBNAIL
from constants.messages import SENDING_VIDEO
from constants.messages import SOMETHING_WENT_WRONG
from constants.messages import USER_NOT_FOUND_CHECK_USERNAME_AND_TRY_AGAIN
from constants.messages import WHAT_DO_YOU_WANT
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
async def get_media_link(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    time.sleep(5)
    await update.message.reply_text(OK_SEND_ME_THE_LINK_YOU_WANT_TO_DOWNLOAD,
                                    reply_markup=back_keyboard)
    return DOWNLOAD_STATE


@send_action(ChatAction.TYPING)
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT,
                                        reply_markup=base_keyboard)
        return HOME_STATE
    client = Client()
    client.delay_range = [1, 3]
    message_is_url = validators.url(message)
    await context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    bot_message = await context.bot.send_message(
        chat_id=update.message.chat_id, text=PROCESSING)
    logged_in_user = login_admin_user_to_instagram(client)
    if not logged_in_user:
        await context.bot.editMessageText(
            message_id=bot_message.message_id,
            chat_id=update.message.chat_id,
            text=SOMETHING_WENT_WRONG,
            reply_markup=back_keyboard,
        )
        return HOME_STATE

    if message_is_url:
        if INSTAGRAM_COM not in message:
            await context.bot.editMessageText(
                message_id=bot_message.message_id,
                chat_id=update.message.chat_id,
                text=PLEASE_SEND_THE_INSTAGRAM_LINK,
            )
        is_link_for_post = False
        is_link_for_reel = False
        if P_SEGMENT in message:
            is_link_for_post = True
        if REEL_SEGMENT in message:
            is_link_for_reel = True
        if STORIES_SEGMENT in message:
            media_type = STORY
        else:
            try:
                media_pk_from_url = client.media_pk_from_url(message)
                await context.bot.editMessageText(
                    message_id=bot_message.message_id,
                    chat_id=update.message.chat_id,
                    text=GETTING_MEDIA_INFORMATION,
                )
                media_info = client.media_info(media_pk_from_url).dict()
                media_type = media_info["media_type"]
                product_type = media_info["product_type"]
            except (MediaNotFound, UnknownError, ValueError):
                if is_link_for_post or is_link_for_reel:
                    await context.bot.deleteMessage(
                        message_id=bot_message.message_id,
                        chat_id=update.message.chat_id,
                    )
                    await context.bot.send_chat_action(
                        chat_id=update.effective_message.chat_id,
                        action=ChatAction.TYPING,
                    )
                    await context.bot.send_message(
                        chat_id=update.effective_message.chat_id,
                        text=MEDIA_NOT_FOUND,
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
                else:
                    regex = r"(?<=instagram.com\/)[A-Za-z0-9_.]+"
                    username = re.findall(regex, message)[0]
                    try:
                        user_data = client.user_info_by_username(
                            username).dict()
                    except UserNotFound:
                        await context.bot.deleteMessage(
                            message_id=bot_message.message_id,
                            chat_id=update.message.chat_id,
                        )
                        await update.message.reply_text(
                            LINK_IS_INVALID,
                            reply_markup=base_keyboard,
                        )
                        return HOME_STATE
                    await context.bot.deleteMessage(
                        message_id=bot_message.message_id,
                        chat_id=update.message.chat_id,
                    )
                    user_profile_picture_url = user_data["profile_pic_url_hd"]
                    await update.effective_user.send_photo(
                        photo=user_profile_picture_url,
                        reply_markup=base_keyboard)
                    return HOME_STATE
        if media_type == PHOTO:
            await context.bot.deleteMessage(
                message_id=bot_message.message_id,
                chat_id=update.message.chat_id,
            )
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=ChatAction.UPLOAD_PHOTO)
            await update.effective_user.send_photo(
                photo=media_info["thumbnail_url"],
                caption=media_info["caption_text"],
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        elif (media_type == VIDEO and product_type == IS_FEED
              or media_type == IGTV and product_type == IS_IGTV
              or media_type == REEL and product_type == IS_CLIPS):
            await context.bot.deleteMessage(
                message_id=bot_message.message_id,
                chat_id=update.message.chat_id,
            )
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=ChatAction.UPLOAD_VIDEO)
            await update.effective_user.send_video(
                video=media_info["video_url"],
                caption=media_info["caption_text"],
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        elif media_type == ALBUM:
            await context.bot.deleteMessage(
                message_id=bot_message.message_id,
                chat_id=update.message.chat_id,
            )
            for media in media_info["resources"]:
                if media["video_url"] is not None:
                    await context.bot.send_chat_action(
                        chat_id=update.effective_message.chat_id,
                        action=ChatAction.UPLOAD_VIDEO,
                    )
                    await update.effective_user.send_video(
                        video=media["video_url"])
                else:
                    await context.bot.send_chat_action(
                        chat_id=update.effective_message.chat_id,
                        action=ChatAction.UPLOAD_PHOTO,
                    )
                    await update.effective_user.send_photo(
                        photo=media["thumbnail_url"])
            await update.effective_user.send_message(
                text=media_info["caption_text"], reply_markup=base_keyboard)
            return HOME_STATE
        elif media_type == STORY:
            try:
                story_pk_from_url = client.story_pk_from_url(message)
                await context.bot.editMessageText(
                    chat_id=update.message.chat_id,
                    message_id=bot_message.message_id,
                    text=GETTING_STORY_INFORMATION,
                )
                story_info = client.story_info(story_pk_from_url)

                if story_info.video_url is None:
                    await context.bot.editMessageText(
                        chat_id=update.message.chat_id,
                        message_id=bot_message.message_id,
                        text=SENDING_THUMBNAIL,
                    )
                    await context.bot.send_chat_action(
                        chat_id=update.effective_message.chat_id,
                        action=ChatAction.UPLOAD_PHOTO,
                    )
                    await update.effective_user.send_photo(
                        photo=story_info.thumbnail_url,
                        reply_markup=base_keyboard,
                    )
                    await context.bot.deleteMessage(
                        message_id=bot_message.message_id,
                        chat_id=update.message.chat_id,
                    )
                else:
                    await context.bot.editMessageText(
                        chat_id=update.message.chat_id,
                        message_id=bot_message.message_id,
                        text=SENDING_THUMBNAIL,
                    )
                    await context.bot.send_chat_action(
                        chat_id=update.effective_message.chat_id,
                        action=ChatAction.UPLOAD_PHOTO,
                    )
                    await update.effective_user.send_photo(
                        photo=story_info.thumbnail_url,
                        reply_markup=base_keyboard,
                    )
                    await context.bot.editMessageText(
                        chat_id=update.message.chat_id,
                        message_id=bot_message.message_id,
                        text=SENDING_VIDEO,
                    )
                    await context.bot.send_chat_action(
                        chat_id=update.effective_message.chat_id,
                        action=ChatAction.UPLOAD_VIDEO,
                    )
                    await update.effective_user.send_video(
                        video=story_info.video_url,
                        reply_markup=base_keyboard,
                    )
                    await context.bot.deleteMessage(
                        message_id=bot_message.message_id,
                        chat_id=update.message.chat_id,
                    )
                return HOME_STATE
            except MediaNotFound:
                await context.bot.editMessageText(
                    chat_id=update.message.chat_id,
                    message_id=bot_message.message_id,
                    text=MEDIA_NOT_FOUND,
                    reply_markup=base_keyboard,
                )
                return HOME_STATE
        else:
            await update.message.reply_text(LINK_IS_INVALID,
                                            reply_markup=back_keyboard)
            return HOME_STATE
    elif message.startswith("@"):
        username = message.split("@")[1]
        try:
            await context.bot.editMessageText(
                message_id=bot_message.message_id,
                chat_id=update.message.chat_id,
                text=GETTING_PROFILE_INFORMATION,
            )
            user_data = client.user_info_by_username(username).dict()
            await context.bot.deleteMessage(
                message_id=bot_message.message_id,
                chat_id=update.message.chat_id,
            )
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=ChatAction.UPLOAD_PHOTO)
            user_profile_picture_url = user_data["profile_pic_url_hd"]
            await update.effective_user.send_photo(
                photo=user_profile_picture_url, reply_markup=base_keyboard)
            return HOME_STATE
        except UserNotFound:
            await context.bot.deleteMessage(message_id=bot_message.message_id,
                                            chat_id=update.message.chat_id)
            await update.message.reply_text(
                USER_NOT_FOUND_CHECK_USERNAME_AND_TRY_AGAIN,
                reply_markup=back_keyboard)
    else:
        await update.message.reply_text(LINK_IS_INVALID,
                                        reply_markup=back_keyboard)
