from logging import getLogger

from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import filters
from telegram.ext import MessageHandler

from commands import admin
from commands import download
from commands import insight
from commands import login
from commands import lottery
from commands import privacy
from commands import rule
from commands import start
from commands import upload
from constants.keys import BACK_KEY
from constants.keys import BACK_TO_HOME_KEY
from constants.keys import DOWNLOAD_KEY
from constants.keys import INSIGHT_KEY
from constants.keys import LOGIN_KEY
from constants.keys import LOTTERY_KEY
from constants.keys import LOTTERY_WITH_COMMENTS_LIST
from constants.keys import LOTTERY_WITH_LIKES_LIST
from constants.keys import PRIVACY_KEY
from constants.keys import SEND_MESSAGE_TO_ALL_USER_KEY
from constants.keys import UPLOAD_KEY
from constants.keys import USER_COUNT_KEY
from constants.states import ADMIN_STATE
from constants.states import DOWNLOAD_STATE
from constants.states import HOME_STATE
from constants.states import INSIGHT_STATE
from constants.states import IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN
from constants.states import IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN_IN_UPLOAD
from constants.states import LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE
from constants.states import LOGIN_STATE
from constants.states import LOGIN_WITH_TWO_FACTOR_AUTHENTICATION
from constants.states import LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD
from constants.states import LOTTERY
from constants.states import SEND_MESSAGE_TO_ALL_USER
from constants.states import SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT
from constants.states import SET_MEDIA_AND_GET_CAPTION
from constants.states import SET_MEDIA_TYPE_AND_GET_MEDIA
from constants.states import SET_POST_LINK_AND_GET_TYPE_OF_LOTTERY
from constants.states import SET_TITLE_OF_IGTV_AND_GET_CAPTION
from constants.states import START_STATE
from constants.states import VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM

# Init logger

logger = getLogger(__name__)


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", rule.rule)],
        states={
            # start ==>
            START_STATE: [MessageHandler(filters.TEXT, start.start)],
            # home ==>
            HOME_STATE: [
                MessageHandler(filters.Regex(f"^{LOGIN_KEY}$"),
                               login.get_login_data),
                MessageHandler(filters.Regex(f"^{DOWNLOAD_KEY}$"),
                               download.get_media_link),
                MessageHandler(filters.Regex(f"^{UPLOAD_KEY}$"),
                               upload.get_login_information),
                MessageHandler(filters.Regex(f"^{INSIGHT_KEY}$"),
                               insight.get_media_link),
                MessageHandler(filters.Regex(f"^{PRIVACY_KEY}$"),
                               privacy.privacy),
                MessageHandler(
                    filters.Regex(f"^{LOTTERY_KEY}$"),
                    lottery.entry_point_and_get_post_link,
                ),
                CommandHandler("admin", admin.admin),
                CommandHandler("start", start.start),
                CommandHandler("privacy", privacy.privacy),
            ],
            # login ==>
            LOGIN_STATE: [MessageHandler(filters.TEXT, login.login)],
            LOGIN_WITH_TWO_FACTOR_AUTHENTICATION: [
                MessageHandler(filters.TEXT,
                               login.login_with_two_factor_authentication)
            ],
            IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN:
            [MessageHandler(filters.TEXT, login.remember_me)],
            # download ==>
            DOWNLOAD_STATE: [MessageHandler(filters.TEXT, download.download)],
            # insight ==>
            INSIGHT_STATE: [MessageHandler(filters.TEXT, insight.insight)],
            # start the upload operation section ==>
            IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN_IN_UPLOAD:
            [MessageHandler(filters.TEXT, upload.remember_me)],
            LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD: [
                MessageHandler(filters.TEXT,
                               upload.login_with_two_factor_authentication)
            ],
            LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE: [
                MessageHandler(filters.TEXT,
                               upload.login_attempt_and_get_media_type)
            ],
            SET_MEDIA_TYPE_AND_GET_MEDIA: [
                MessageHandler(filters.TEXT,
                               upload.set_media_type_and_get_media)
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
                    filters.TEXT,
                    upload.set_caption_and_asking_to_confirm_the_content)
            ],
            SET_TITLE_OF_IGTV_AND_GET_CAPTION: [
                MessageHandler(filters.TEXT,
                               upload.set_title_of_igtv_and_get_caption)
            ],
            VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM: [
                MessageHandler(filters.TEXT,
                               upload.verify_content_and_upload_on_instagram)
            ],
            # end the upload operation section <==
            # start admin section ==>
            ADMIN_STATE: [
                MessageHandler(filters.Regex(f"^{USER_COUNT_KEY}$"),
                               admin.user_count),
                MessageHandler(filters.Regex(f"^{BACK_TO_HOME_KEY}$"),
                               admin.back_to_home),
                MessageHandler(
                    filters.Regex(f"^{SEND_MESSAGE_TO_ALL_USER_KEY}$"),
                    admin.get_message_for_send_to_all_user,
                ),
            ],
            SEND_MESSAGE_TO_ALL_USER:
            [MessageHandler(filters.TEXT, admin.send_message_to_all_user)],
            # end of the admin section <==
            # start lottery section ==>
            SET_POST_LINK_AND_GET_TYPE_OF_LOTTERY: [
                MessageHandler(filters.TEXT,
                               lottery.set_post_link_and_get_type_of_lottery),
            ],
            LOTTERY: [
                MessageHandler(
                    filters.Regex(f"^{LOTTERY_WITH_LIKES_LIST}$"),
                    lottery.lottery_with_likes_list,
                ),
                MessageHandler(
                    filters.Regex(f"^{LOTTERY_WITH_COMMENTS_LIST}$"),
                    lottery.lottery_with_comments_list,
                ),
                MessageHandler(
                    filters.Regex(f"^{BACK_KEY}$"),
                    start.start,
                ),
            ]
            # end of lottery section <==
        },
        fallbacks=[],
        persistent=True,
    )
    return conversation_handler
