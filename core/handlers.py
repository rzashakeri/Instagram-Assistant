
from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler, MessageHandler, filters
)

from bot.start import start
from core.constants import CHOOSING

# Init logger
logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={},
        fallbacks=[],
    )
    return conversation_handler
