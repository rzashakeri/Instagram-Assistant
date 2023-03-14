# encoding: utf-8

from logging import getLogger

from telegram import Update
from telegram.ext import ContextTypes

from core.keyboards import main_keyboard
from core.constants import CHOOSING

# Init logger
logger = getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    welcome_message: str = (
        "Hi, Welcome To Instagram in Telegram Bot, "
        "With this robot you can do whatever you do "
        "on Instagram using the telegram with additional features."
    )
    await update.message.reply_text(
        welcome_message, reply_markup=main_keyboard
    )
    return CHOOSING
