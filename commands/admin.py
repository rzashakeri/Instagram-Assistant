# encoding: utf-8
import time
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from configurations.settings import ADMIN_TELEGRAM_USER_ID
from connectors.postgresql import get_request_count
from connectors.postgresql import get_user_count
from connectors.postgresql import get_user_id
from connectors.postgresql import get_user_request_insight
from connectors.postgresql import get_user_signup_insight
from constants.keys import BACK_KEY
from constants.messages import INSIGHT_OF_ROBOT
from constants.messages import SEND_YOUR_MESSAGE
from constants.messages import USER_COUNT
from constants.messages import WELCOME_TO_ADMIN
from constants.messages import WELCOME_TO_HOME
from constants.messages import YOUR_MESSAGE_WAS_SENT
from constants.states import ADMIN_STATE
from constants.states import HOME_STATE
from constants.states import SEND_MESSAGE_TO_ALL_USER
from core.keyboards import admin_keyboard
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from utils.decorators import restricted
from utils.decorators import send_action

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
async def user_count(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> str:
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
async def back_to_home(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> str:
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
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """get user count"""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        SEND_YOUR_MESSAGE,
        reply_markup=back_keyboard,
    )
    return SEND_MESSAGE_TO_ALL_USER


@restricted
@send_action(ChatAction.TYPING)
async def send_message_to_all_user(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE) -> str:
    """get user count"""
    # pylint: disable=unused-argument
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text("what do you want ?",
                                        reply_markup=admin_keyboard)
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
async def get_insight(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> str:
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
            all_request_count=all_request_count[0][0],
            yearly_request_count=last_year_request_count[0][1],
            monthly_request_count=last_month_request_count[0][1],
            daily_request_count=last_day_request_count[0][1],
        ),
        reply_markup=admin_keyboard,
    )
    return ADMIN_STATE


def daily_insight(context):
    """Send Daily Insight To Admin"""
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
    context.bot.send_message(
        chat_id=ADMIN_TELEGRAM_USER_ID,
        text=INSIGHT_OF_ROBOT.format(
            all_user_count=all_user_count,
            yearly_user_count=last_year_user_count[0][1],
            monthly_user_count=last_month_user_count[0][1],
            daily_user_count=last_day_user_count[0][1],
            all_request_count=all_request_count[0][0],
            yearly_request_count=last_year_request_count[0][1],
            monthly_request_count=last_month_request_count[0][1],
            daily_request_count=last_day_request_count[0][1],
        ),
    )
