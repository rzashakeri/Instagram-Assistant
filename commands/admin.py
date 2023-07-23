# encoding: utf-8
import time
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from connectors.postgresql import (get_request_count, get_user_count,
                                   get_user_id, get_user_request_insight,
                                   get_user_signup_insight)
from constants.keys import BACK_KEY
from constants.messages import (INSIGHT_OF_ROBOT, SEND_YOUR_MESSAGE,
                                USER_COUNT, WELCOME_TO_ADMIN, WELCOME_TO_HOME,
                                YOUR_MESSAGE_WAS_SENT)
from constants.states import ADMIN_STATE, HOME_STATE, SEND_MESSAGE_TO_ALL_USER
from core.keyboards import admin_keyboard, back_keyboard, base_keyboard
from utils.decorators import restricted, send_action

# Init logger
logger = getLogger(__name__)


@restricted
@send_action(ChatAction.TYPING)
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    time.sleep(3)
    await update.message.reply_text(
        WELCOME_TO_ADMIN,
        reply_markup=admin_keyboard,
    )
    return ADMIN_STATE


@restricted
@send_action(ChatAction.TYPING)
async def user_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """get user count"""
    # pylint: disable=unused-argument
    user_count = get_user_count()
    await update.message.reply_text(
        USER_COUNT.format(user_count=user_count),
        reply_markup=admin_keyboard,
    )
    return ADMIN_STATE


@restricted
@send_action(ChatAction.TYPING)
async def back_to_home(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """get user count"""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        WELCOME_TO_HOME,
        reply_markup=base_keyboard,
    )
    return HOME_STATE


@restricted
@send_action(ChatAction.TYPING)
async def get_message_for_send_to_all_user(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """get user count"""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        SEND_YOUR_MESSAGE,
        reply_markup=back_keyboard,
    )
    return SEND_MESSAGE_TO_ALL_USER


@restricted
@send_action(ChatAction.TYPING)
async def send_message_to_all_user(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """get user count"""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(
            "what do you want ?", reply_markup=admin_keyboard
        )
        return ADMIN_STATE
    columns = get_user_id()
    for row in columns:
        for user_id in row:
            await context.bot.send_message(chat_id=user_id, text=message)
    await update.message.reply_text(
        YOUR_MESSAGE_WAS_SENT,
        reply_markup=admin_keyboard,
    )
    return ADMIN_STATE


@restricted
@send_action(ChatAction.TYPING)
async def get_insight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """get user count"""
    # pylint: disable=unused-argument
    all_user_count = get_user_count()
    all_request_count = get_request_count()
    (
        last_day_user_count,
        last_month_user_count,
        last_year_user_count,
    ) = get_user_signup_insight()
    (
        last_day_request_count,
        last_month_request_count,
        last_year_request_count,
    ) = get_user_request_insight()
    await update.message.reply_text(
        INSIGHT_OF_ROBOT.format(
            all_user_count=all_user_count,
            yearly_user_count=last_year_user_count[0][1],
            monthly_user_count=last_month_user_count[0][1],
            daily_user_count=last_day_user_count[0][1],
            all_request_count=all_request_count[0],
            yearly_request_count=last_year_request_count[0][1],
            monthly_request_count=last_month_request_count[0][1],
            daily_request_count=last_day_request_count[0][1],
        ),
        reply_markup=admin_keyboard,
    )
    return ADMIN_STATE
