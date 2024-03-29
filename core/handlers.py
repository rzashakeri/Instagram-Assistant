from logging import getLogger

from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import filters
from telegram.ext import MessageHandler

from commands import admin
from commands import download
from commands import feedback
from commands import insight
from commands import lottery
from commands import privacy
from commands import rule
from commands import start
from commands import upload
from constants.keys import BACK_KEY, RESTART_KEY, SHUT_DOWN_KEY
from constants.keys import BACK_TO_HOME_KEY
from constants.keys import DOWNLOAD_KEY
from constants.keys import FEEDBACK_KEY
from constants.keys import INSIGHT_KEY
from constants.keys import INSIGHT_OF_ROBOT_KEY
from constants.keys import LOTTERY_KEY
from constants.keys import LOTTERY_WITH_COMMENTS_LIST
from constants.keys import LOTTERY_WITH_LIKES_LIST
from constants.keys import PRIVACY_KEY
from constants.keys import SEND_MESSAGE_TO_ALL_USER_KEY
from constants.keys import UPLOAD_KEY
from constants.keys import USER_COUNT_KEY
from constants.states import ADMIN_STATE
from constants.states import DOWNLOAD_STATE
from constants.states import FEEDBACK_STATE
from constants.states import HOME_STATE
from constants.states import INSIGHT_STATE
from constants.states import (
    IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN_IN_UPLOAD,
)
from constants.states import LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE
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


def admin_conversation_handler():
    """admin conversation handler"""
    admin_user_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("admin", admin.admin)],
        states={
            ADMIN_STATE: [
                MessageHandler(
                    filters.Regex(f"^{USER_COUNT_KEY}$"),
                    admin.user_count,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{BACK_TO_HOME_KEY}$"),
                    admin.back_to_home,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{INSIGHT_OF_ROBOT_KEY}$"),
                    admin.get_insight,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{SEND_MESSAGE_TO_ALL_USER_KEY}$"),
                    admin.get_message_for_send_to_all_user,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{SHUT_DOWN_KEY}$"),
                    admin.shutdown_bot,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{RESTART_KEY}$"),
                    admin.restart_bot,
                    block=False,
                ),
            ]
        },
        fallbacks=[],
        name="admin_conversation_handler",
        persistent=True,
    )
    return admin_user_conversation_handler


def base_conversation_handler():
    """Process a /start command."""
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", rule.rule, block=False)],
        states={
            # start ==>
            START_STATE: [MessageHandler(filters.TEXT, start.start, block=False)],
            # home ==>
            HOME_STATE: [
                MessageHandler(
                    filters.Regex(f"^{DOWNLOAD_KEY}$"),
                    download.get_media_link,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{UPLOAD_KEY}$"),
                    upload.get_login_information,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{INSIGHT_KEY}$"),
                    insight.get_media_link,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{PRIVACY_KEY}$"), privacy.privacy, block=False
                ),
                MessageHandler(
                    filters.Regex(f"^{FEEDBACK_KEY}$"),
                    feedback.get_feedback,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{LOTTERY_KEY}$"),
                    lottery.entry_point_and_get_post_link,
                    block=False,
                ),
                CommandHandler("admin", admin.admin, block=False),
                CommandHandler("start", start.start, block=False),
                CommandHandler("privacy", privacy.privacy, block=False),
            ],
            # download ==>
            DOWNLOAD_STATE: [
                MessageHandler(filters.TEXT, download.download, block=False)
            ],
            # insight ==>
            INSIGHT_STATE: [MessageHandler(filters.TEXT, insight.insight, block=False)],
            # start the upload operation section ==>
            IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN_IN_UPLOAD: [
                MessageHandler(filters.TEXT, upload.remember_me, block=False)
            ],
            LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD: [
                MessageHandler(
                    filters.TEXT,
                    upload.login_with_two_factor_authentication,
                    block=False,
                )
            ],
            LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE: [
                MessageHandler(
                    filters.TEXT, upload.login_attempt_and_get_media_type, block=False
                )
            ],
            SET_MEDIA_TYPE_AND_GET_MEDIA: [
                MessageHandler(
                    filters.TEXT, upload.set_media_type_and_get_media, block=False
                )
            ],
            SET_MEDIA_AND_GET_CAPTION: [
                MessageHandler(
                    filters.PHOTO
                    | filters.VIDEO
                    | filters.TEXT
                    | filters.Document.IMAGE
                    | filters.Document.VIDEO,
                    upload.set_media_and_get_caption,
                    block=False,
                )
            ],
            SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT: [
                MessageHandler(
                    filters.TEXT,
                    upload.set_caption_and_asking_to_confirm_the_content,
                    block=False,
                )
            ],
            SET_TITLE_OF_IGTV_AND_GET_CAPTION: [
                MessageHandler(
                    filters.TEXT, upload.set_title_of_igtv_and_get_caption, block=False
                )
            ],
            VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM: [
                MessageHandler(
                    filters.TEXT,
                    upload.verify_content_and_upload_on_instagram,
                    block=False,
                )
            ],
            # end the upload operation section <==
            # start admin section ==>
            ADMIN_STATE: [
                MessageHandler(
                    filters.Regex(f"^{USER_COUNT_KEY}$"),
                    admin.user_count,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{BACK_TO_HOME_KEY}$"),
                    admin.back_to_home,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{INSIGHT_OF_ROBOT_KEY}$"),
                    admin.get_insight,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{SEND_MESSAGE_TO_ALL_USER_KEY}$"),
                    admin.get_message_for_send_to_all_user,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{SHUT_DOWN_KEY}$"),
                    admin.shutdown_bot,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{RESTART_KEY}$"),
                    admin.restart_bot,
                    block=False,
                ),
            ],
            SEND_MESSAGE_TO_ALL_USER: [
                MessageHandler(
                    filters.TEXT, admin.send_message_to_all_user, block=False
                )
            ],
            # end of the admin section <==
            # start lottery section ==>
            SET_POST_LINK_AND_GET_TYPE_OF_LOTTERY: [
                MessageHandler(
                    filters.TEXT,
                    lottery.set_post_link_and_get_type_of_lottery,
                    block=False,
                ),
            ],
            LOTTERY: [
                MessageHandler(
                    filters.Regex(f"^{LOTTERY_WITH_LIKES_LIST}$"),
                    lottery.lottery_with_likes_list,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{LOTTERY_WITH_COMMENTS_LIST}$"),
                    lottery.lottery_with_comments_list,
                    block=False,
                ),
                MessageHandler(
                    filters.Regex(f"^{BACK_KEY}$"), start.start, block=False
                ),
            ],
            # end of the lottery section <==
            # start feedback section
            FEEDBACK_STATE: [
                MessageHandler(filters.TEXT, feedback.send_feedback, block=False)
            ]
            # end of feedback section
        },
        fallbacks=[],
        name="base_conversation_handler",
        persistent=True,
    )
    return conversation_handler
