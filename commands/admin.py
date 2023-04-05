# encoding: utf-8
import time
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from connectors.postgresql import get_user_count
from constants.messages import WELCOME_TO_ADMIN, USER_COUNT
from constants.states import ADMIN_STATE
from core.keyboards import base_keyboard, admin_keyboard

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
