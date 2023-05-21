# encoding: utf-8
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from constants.messages import BOT_UNDER_MAINTENANCE
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def maintenance(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=BOT_UNDER_MAINTENANCE,
    )
