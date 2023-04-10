# encoding: utf-8
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from connectors.postgresql import create_user
from constants.messages import (PRIVACY_MESSAGE, WELCOME_MESSAGE,
                                WELCOME_TO_THE_LOTTERY_SECTION)
from constants.states import HOME_STATE
from core.keyboards import base_keyboard, lottery_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def lottery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        WELCOME_TO_THE_LOTTERY_SECTION,
        reply_markup=lottery_keyboard,
    )
    return HOME_STATE
