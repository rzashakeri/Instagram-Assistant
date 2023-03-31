# encoding: utf-8

from logging import getLogger

from telegram import Update
from telegram.ext import ContextTypes

from configurations.settings import TELEGRAM_USER_ID
from constants.messages import WELCOME_TO_ADMIN
from constants.states import HOME_STATE
from core.keyboards import base_keyboard

from utils import restricted

# Init logger
logger = getLogger(__name__)


@restricted
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        WELCOME_TO_ADMIN,
        reply_markup=base_keyboard,
    )
    return HOME_STATE
