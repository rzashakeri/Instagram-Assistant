# encoding: utf-8

from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from constants.messages import WELCOME_MESSAGE
from constants.states import HOME_STATE
from core.keyboards import base_keyboard

# Init logger
from utils.decorators import send_action

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        WELCOME_MESSAGE.format(first_name=update.effective_user.first_name),
        reply_markup=base_keyboard,
    )
    return HOME_STATE
