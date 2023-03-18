# encoding: utf-8

from logging import getLogger

from telegram import Update
from telegram.ext import ContextTypes
import validators
from core.constants import HOME, BACK
from core.keyboards import base_keyboard, back_keyboard

# Init logger
logger = getLogger(__name__)


async def get_media_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    welcome_message: str = "OK, send me the link you want to download from Instagram"
    await update.message.reply_text(
        welcome_message, reply_markup=back_keyboard
    )
    return HOME


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""

    message = update.message.text
    if message == BACK:
        await update.message.reply_text(
            "what do you want ?", reply_markup=base_keyboard
        )
        return HOME
    message_is_link = validators.email(message)
