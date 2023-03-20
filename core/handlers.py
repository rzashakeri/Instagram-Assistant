from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler, MessageHandler, filters,
)

from commands.download import get_media_link, download
from commands.login import get_login_data, login
from commands.start import start

# Init logger
from commands.upload import get_login_data_for_upload_media, login_to_instagram_for_upload_media, get_file_for_upload_in_instagram

from constants.keyboards import LOGIN_KEY, DOWNLOAD_KEY, UPLOAD_KEY
from constants.states import HOME_STATE, LOGIN_STATE, DOWNLOAD_STATE, UPLOAD_STATE, LOGIN_TO_INSTAGRAM_FOR_UPLOAD_MEDIA_STATE, GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE, GET_CAPTION_OF_POST_FOR_UPLOAD_IN_INSTAGRAM_STATE

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HOME_STATE: [
                MessageHandler(filters.Regex(f"^{LOGIN_KEY}$"), get_login_data),
                MessageHandler(filters.Regex(f"^{DOWNLOAD_KEY}$"), get_media_link),
                MessageHandler(filters.Regex(f"^{UPLOAD_KEY}$"), get_login_data_for_upload_media),
            ],
            LOGIN_STATE: [
                MessageHandler(filters.TEXT, login)
            ],
            DOWNLOAD_STATE: [
                MessageHandler(filters.TEXT, download)
            ],
            # upload operation
            LOGIN_TO_INSTAGRAM_FOR_UPLOAD_MEDIA_STATE: [
                MessageHandler(filters.TEXT, login_to_instagram_for_upload_media)
            ],
            GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE: [
                MessageHandler(filters.TEXT, get_file_for_upload_in_instagram)
            ],
            GET_CAPTION_OF_POST_FOR_UPLOAD_IN_INSTAGRAM_STATE: [
                MessageHandler(filters.TEXT, get_file_for_upload_in_instagram)
            ]
        },
        fallbacks=[],
    )
    return conversation_handler
