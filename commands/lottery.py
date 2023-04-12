# encoding: utf-8
import random
import time
from logging import getLogger

import validators
from instagrapi import Client
from instagrapi.exceptions import MediaNotFound
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from commands.login import login_admin_user_to_instagram
from connectors.postgresql import create_user
from constants import PROCESSING
from constants.keys import BACK_KEY
from constants.messages import LINK_IS_INVALID
from constants.messages import PRIVACY_MESSAGE
from constants.messages import WELCOME_MESSAGE
from constants.messages import WELCOME_TO_THE_LOTTERY_SECTION
from constants.messages import WELL_YOU_WANT_TO_DO_THE_LOTTERY_ON_WHAT_BASIS
from constants.messages import WHAT_DO_YOU_WANT
from constants.states import HOME_STATE
from constants.states import LOTTERY
from constants.states import SET_POST_LINK_AND_GET_TYPE_OF_LOTTERY
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from core.keyboards import lottery_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)

POST_LINK = None
CLIENT = Client()
CLIENT.delay_range = [1, 3]


@send_action(ChatAction.TYPING)
async def entry_point_and_get_post_link(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        WELCOME_TO_THE_LOTTERY_SECTION,
        reply_markup=back_keyboard,
    )
    return SET_POST_LINK_AND_GET_TYPE_OF_LOTTERY


@send_action(ChatAction.TYPING)
async def set_post_link_and_get_type_of_lottery(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    message_is_url = validators.url(message)
    if message_is_url:
        global POST_LINK
        POST_LINK = message
        await update.message.reply_text(
            WELL_YOU_WANT_TO_DO_THE_LOTTERY_ON_WHAT_BASIS, reply_markup=lottery_keyboard
        )
        return LOTTERY
    await update.message.reply_text(LINK_IS_INVALID, reply_markup=back_keyboard)


@send_action(ChatAction.TYPING)
async def lottery_with_likes_list(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    try:
        login_admin_user_to_instagram(CLIENT)

        # start getting post information ==>
        processing_message = await context.bot.send_message(
            chat_id=update.message.chat_id, text=PROCESSING
        )
        media_pk_from_url = CLIENT.media_pk_from_url(POST_LINK)
        media_id = CLIENT.media_id(media_pk_from_url)
        await context.bot.deleteMessage(
            message_id=processing_message.message_id, chat_id=update.message.chat_id
        )

        # getting like the list from instagram ==>
        getting_likes_list_message = await context.bot.send_message(
            chat_id=update.message.chat_id, text="Grabbing Likes List ..."
        )
        media_likers = CLIENT.media_likers(media_id)
        await context.bot.deleteMessage(
            message_id=getting_likes_list_message.message_id,
            chat_id=update.message.chat_id,
        )

        # find winner ==>
        find_winner_message = await context.bot.send_message(
            chat_id=update.message.chat_id, text="Finding Winner ... 🎖️"
        )
        winner = random.choice(media_likers)
        await context.bot.deleteMessage(
            message_id=find_winner_message.message_id, chat_id=update.message.chat_id
        )

        countdown_message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Countdown to introduce the winner 🕐",
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=countdown_message.message_id, chat_id=update.message.chat_id
        )

        number_three = await context.bot.send_message(
            chat_id=update.message.chat_id, text="3️⃣"
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=number_three.message_id, chat_id=update.message.chat_id
        )

        number_two = await context.bot.send_message(
            chat_id=update.message.chat_id, text="2️⃣"
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=number_two.message_id, chat_id=update.message.chat_id
        )

        number_one = await context.bot.send_message(
            chat_id=update.message.chat_id, text="1️⃣"
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=number_one.message_id, chat_id=update.message.chat_id
        )
        await context.bot.send_photo(
            chat_id=update.message.chat_id, photo=winner.profile_pic_url
        )
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"https://instagram.com/{winner.username}",
            reply_markup=base_keyboard,
        )
        return HOME_STATE
    except MediaNotFound:
        await update.message.reply_text(
            "media not found, check your link and try again", reply_markup=base_keyboard
        )


@send_action(ChatAction.TYPING)
async def lottery_with_comments_list(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    try:
        login_admin_user_to_instagram(CLIENT)

        # start getting post information ==>
        processing_message = await context.bot.send_message(
            chat_id=update.message.chat_id, text=PROCESSING
        )
        media_pk_from_url = CLIENT.media_pk_from_url(POST_LINK)
        media_id = CLIENT.media_id(media_pk_from_url)
        await context.bot.deleteMessage(
            message_id=processing_message.message_id, chat_id=update.message.chat_id
        )

        # getting like the list from instagram ==>
        getting_comments_list_message = await context.bot.send_message(
            chat_id=update.message.chat_id, text="Grabbing Comments List ..."
        )
        media_comments = CLIENT.media_comments(media_id)
        await context.bot.deleteMessage(
            message_id=getting_comments_list_message.message_id,
            chat_id=update.message.chat_id,
        )

        # find winner ==>
        find_winner_message = await context.bot.send_message(
            chat_id=update.message.chat_id, text="Finding Winner ... 🎖️"
        )
        winner = random.choice(media_comments)
        await context.bot.deleteMessage(
            message_id=find_winner_message.message_id, chat_id=update.message.chat_id
        )

        countdown_message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Countdown to introduce the winner 🕐",
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=countdown_message.message_id, chat_id=update.message.chat_id
        )

        number_three = await context.bot.send_message(
            chat_id=update.message.chat_id, text="3️⃣"
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=number_three.message_id, chat_id=update.message.chat_id
        )

        number_two = await context.bot.send_message(
            chat_id=update.message.chat_id, text="2️⃣"
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=number_two.message_id, chat_id=update.message.chat_id
        )

        number_one = await context.bot.send_message(
            chat_id=update.message.chat_id, text="1️⃣"
        )
        time.sleep(1)
        await context.bot.deleteMessage(
            message_id=number_one.message_id, chat_id=update.message.chat_id
        )
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=winner.user.profile_pic_url,
            caption=f"winner username: https://instagram.com/{winner.user.username}\nwinner comment: {winner.text}",
            reply_markup=base_keyboard,
        )
        return HOME_STATE
    except MediaNotFound:
        await update.message.reply_text(
            "media not found, check your link and try again", reply_markup=base_keyboard
        )
