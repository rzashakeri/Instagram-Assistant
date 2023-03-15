from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler, MessageHandler, filters,
)

from commands.login import get_login_data, login
from commands.start import start

# Init logger
from core.constants import HOME, LOGIN, LOGIN_TO_INSTAGRAM

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HOME: [
                MessageHandler(filters.Regex(f"^{LOGIN}$"), get_login_data)
            ],
            LOGIN_TO_INSTAGRAM: [
                MessageHandler(filters.TEXT, login)
            ]
        },
        fallbacks=[],
    )
    return conversation_handler
