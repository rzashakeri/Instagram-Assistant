# encoding: utf-8
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from configurations.settings import ADMIN_TELEGRAM_USER_ID
from constants.keys import BACK_KEY
from constants.messages import (FEEDBACK_MESSAGE, NEW_TEXT_MESSAGE,
                                WHAT_DO_YOU_WANT, YOUR_MESSAGE_WAS_SENT)
from constants.states import FEEDBACK_STATE, HOME_STATE
from core.keyboards import back_keyboard, base_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def get_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=FEEDBACK_MESSAGE,
        reply_markup=back_keyboard,
    )
    return FEEDBACK_STATE


@send_action(ChatAction.TYPING)
async def send_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username

    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    await context.bot.send_message(
        chat_id=ADMIN_TELEGRAM_USER_ID,
        text=NEW_TEXT_MESSAGE.format(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            message=message,
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=YOUR_MESSAGE_WAS_SENT,
        reply_markup=base_keyboard,
    )
    return HOME_STATE
