from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
)

from commands.start import start

# Init logger
logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={},
        fallbacks=[],
        map_to_parent={},
    )
    return conversation_handler
