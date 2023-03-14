
from logging import getLogger

from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler, MessageHandler, filters,
)

from bot.start import start
from core.constants import CHOOSING, TYPING_CHOICE, TYPING_REPLY

# Init logger
logger = getLogger(__name__)


def conversation():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [

            ],
            TYPING_CHOICE: [],
            TYPING_REPLY: [],
        },
        fallbacks=[],
    )
    return conversation_handler
