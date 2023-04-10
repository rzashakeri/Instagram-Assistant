# encoding: utf-8
from logging import getLogger

import validators
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from connectors.postgresql import create_user
from constants.keys import BACK_KEY
from constants.messages import (
    LINK_IS_INVALID,
    WELL_YOU_WANT_TO_DO_THE_LOTTERY_ON_WHAT_BASIS,
)
from constants.messages import PRIVACY_MESSAGE
from constants.messages import WELCOME_MESSAGE
from constants.messages import WELCOME_TO_THE_LOTTERY_SECTION
from constants.messages import WHAT_DO_YOU_WANT
from constants.states import HOME_STATE, LOTTERY
from constants.states import SET_POST_LINK_AND_GET_TYPE_OF_LOTTERY
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from core.keyboards import lottery_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)

POST_LINK = None


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
