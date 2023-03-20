from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler, MessageHandler, filters,
)

from commands.download import get_media_link, download
from commands.login import get_login_data, login
from commands.start import start

# Init logger

from constants.keyboards import LOGIN_KEY, DOWNLOAD_KEY
from constants.states import HOME_STATE, LOGIN_STATE, DOWNLOAD_STATE

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HOME_STATE: [
                MessageHandler(filters.Regex(f"^{LOGIN_KEY}$"), get_login_data),
                MessageHandler(filters.Regex(f"^{DOWNLOAD_KEY}$"), get_media_link)
            ],
            LOGIN_STATE: [
                MessageHandler(filters.TEXT, login)
            ],
            DOWNLOAD_STATE: [
                MessageHandler(filters.TEXT, download)
            ]
        },
        fallbacks=[],
    )
    return conversation_handler
