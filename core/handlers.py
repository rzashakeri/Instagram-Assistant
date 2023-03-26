from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands.download import get_media_link, download
from commands.login import get_login_data, login
from commands.start import start

# Init logger
from commands import upload
from commands.upload import get_media_type, set_media_type
from constants.keyboards import LOGIN_KEY, DOWNLOAD_KEY, UPLOAD_KEY
from constants.states import (
    HOME_STATE,
    LOGIN_STATE,
    DOWNLOAD_STATE,
    UPLOAD_STATE,
    LOGIN_TO_INSTAGRAM_FOR_UPLOAD_MEDIA_STATE,
    GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE,
    GET_CAPTION_OF_POST_FOR_UPLOAD_IN_INSTAGRAM_STATE, GET_MEDIA_TYPE_STATE, SET_MEDIA_TYPE_STATE,
)

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HOME_STATE: [
                MessageHandler(filters.Regex(f"^{LOGIN_KEY}$"), get_login_data),
                MessageHandler(filters.Regex(f"^{DOWNLOAD_KEY}$"), get_media_link),
                MessageHandler(
                    filters.Regex(f"^{UPLOAD_KEY}$"), upload.get_login_information
                ),
            ],
            LOGIN_STATE: [MessageHandler(filters.TEXT, login)],
            DOWNLOAD_STATE: [MessageHandler(filters.TEXT, download)],
            # upload operation
            LOGIN_TO_INSTAGRAM_FOR_UPLOAD_MEDIA_STATE: [
                MessageHandler(filters.TEXT, upload.login)
            ],
            GET_MEDIA_TYPE_STATE: [
                MessageHandler(filters.TEXT, get_media_type)
            ],
            SET_MEDIA_TYPE_STATE: [
                MessageHandler(filters.TEXT, set_media_type)
            ],
            GET_FILE_FOR_UPLOAD_IN_INSTAGRAM_STATE: [
                MessageHandler(
                    filters.PHOTO
                    | filters.VIDEO
                    | filters.TEXT
                    | filters.Document.IMAGE
                    | filters.Document.VIDEO,
                    upload.get_media,
                )
            ],
            GET_CAPTION_OF_POST_FOR_UPLOAD_IN_INSTAGRAM_STATE: [
                MessageHandler(filters.TEXT, upload.get_caption)
            ],
        },
        fallbacks=[],
    )
    return conversation_handler
