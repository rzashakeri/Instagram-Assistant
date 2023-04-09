from logging import getLogger

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Init logger
from commands import start
from commands import login
from commands import admin
from commands import upload
from commands import privacy
from commands import insight
from commands import lottery
from commands import download
from constants.keys import (
    LOGIN_KEY,
    DOWNLOAD_KEY,
    UPLOAD_KEY,
    INSIGHT_KEY,
    USER_COUNT_KEY,
    BACK_TO_HOME_KEY,
    SEND_MESSAGE_TO_ALL_USER_KEY, PRIVACY_KEY, LOTTERY_KEY,
)
from constants.states import (
    HOME_STATE,
    LOGIN_STATE,
    DOWNLOAD_STATE,
    LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE,
    SET_MEDIA_TYPE_AND_GET_MEDIA,
    SET_MEDIA_AND_GET_CAPTION,
    SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT,
    VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM,
    INSIGHT_STATE,
    ADMIN_STATE, SEND_MESSAGE_TO_ALL_USER, LOTTERY_STATE,
)

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start.start)],
        states={
            HOME_STATE: [
                MessageHandler(filters.Regex(f"^{LOGIN_KEY}$"), login.get_login_data),
                MessageHandler(
                    filters.Regex(f"^{DOWNLOAD_KEY}$"), download.get_media_link
                ),
                MessageHandler(
                    filters.Regex(f"^{UPLOAD_KEY}$"), upload.get_login_information
                ),
                MessageHandler(
                    filters.Regex(f"^{INSIGHT_KEY}$"), insight.get_media_link
                ),
                MessageHandler(
                    filters.Regex(f"^{PRIVACY_KEY}$"), privacy.privacy
                ),
                MessageHandler(
                    filters.Regex(f"^{LOTTERY_KEY}$"), lottery.lottery
                ),
                CommandHandler("admin", admin.admin),
            ],
            LOGIN_STATE: [MessageHandler(filters.TEXT, login.login)],
            DOWNLOAD_STATE: [MessageHandler(filters.TEXT, download.download)],
            INSIGHT_STATE: [MessageHandler(filters.TEXT, insight.insight)],
            # start the upload operation section ==>
            LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE: [
                MessageHandler(filters.TEXT, upload.login_attempt_and_get_media_type)
            ],
            SET_MEDIA_TYPE_AND_GET_MEDIA: [
                MessageHandler(filters.TEXT, upload.set_media_type_and_get_media)
            ],
            SET_MEDIA_AND_GET_CAPTION: [
                MessageHandler(
                    filters.PHOTO
                    | filters.VIDEO
                    | filters.TEXT
                    | filters.Document.IMAGE
                    | filters.Document.VIDEO,
                    upload.set_media_and_get_caption,
                )
            ],
            SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT: [
                MessageHandler(
                    filters.TEXT, upload.set_caption_and_asking_to_confirm_the_content
                )
            ],
            VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM: [
                MessageHandler(
                    filters.TEXT, upload.verify_content_and_upload_on_instagram
                )
            ],
            # end the upload operation section <==
            # start admin section ==>
            ADMIN_STATE: [
                MessageHandler(filters.Regex(f"^{USER_COUNT_KEY}$"), admin.user_count),
                MessageHandler(
                    filters.Regex(f"^{BACK_TO_HOME_KEY}$"), admin.back_to_home
                ),
                MessageHandler(
                    filters.Regex(f"^{SEND_MESSAGE_TO_ALL_USER_KEY}$"),
                    admin.get_message_for_send_to_all_user,
                ),
            ],
            SEND_MESSAGE_TO_ALL_USER: [
                MessageHandler(
                    filters.TEXT, admin.send_message_to_all_user
                )
            ],
            # end of admin section <==
            # start lottery section ==>
            LOTTERY_STATE:[]
            # end of lottery section <==
        },
        fallbacks=[],
    )
    return conversation_handler
