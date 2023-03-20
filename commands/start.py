# encoding: utf-8

from logging import getLogger

from telegram import Update
from telegram.ext import ContextTypes

from core.constants import HOME, WELCOME_MESSAGE
from core.keyboards import base_keyboard

# Init logger
logger = getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    await update.message.reply_text(
        WELCOME_MESSAGE.format(first_name=update.effective_user.first_name),
        reply_markup=base_keyboard,
    )
    return HOME
