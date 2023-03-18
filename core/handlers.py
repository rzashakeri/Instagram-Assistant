from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler, MessageHandler, filters,
)

from commands.download import get_media_link, download
from commands.login import get_login_data, login
from commands.start import start

# Init logger
from core.constants import HOME, LOGIN, LOGIN_TO_INSTAGRAM, DOWNLOAD, DOWNLOAD_MEDIA

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HOME: [
                MessageHandler(filters.Regex(f"^{LOGIN}$"), get_login_data),
                MessageHandler(filters.Regex(f"^{DOWNLOAD}$"), get_media_link)
            ],
            LOGIN_TO_INSTAGRAM: [
                MessageHandler(filters.TEXT, login)
            ],
            DOWNLOAD_MEDIA: [
                MessageHandler(filters.TEXT, download)
            ]
        },
        fallbacks=[],
    )
    return conversation_handler
