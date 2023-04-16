# encoding: utf-8
import os
import time
from logging import getLogger

from instagrapi import Client
from instagrapi.exceptions import ClientError
from instagrapi.exceptions import ClipNotUpload
from instagrapi.exceptions import IGTVNotUpload
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import PhotoNotUpload
from instagrapi.exceptions import TwoFactorRequired
from instagrapi.exceptions import UnknownError
from instagrapi.exceptions import VideoNotUpload
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

import constants
from constants import BACK
from constants import DOCUMENT
from constants import LOGIN
from constants import PROCESSING
from constants import YES
from constants.keys import BACK_KEY
from constants.keys import UPLOAD_ALBUM_KEY
from constants.keys import UPLOAD_IGTV_KEY
from constants.keys import UPLOAD_PHOTO_KEY
from constants.keys import UPLOAD_REELS_KEY
from constants.keys import UPLOAD_VIDEO_KEY
from constants.media_types import ALBUM
from constants.media_types import IGTV
from constants.media_types import PHOTO
from constants.media_types import REEL
from constants.media_types import VIDEO
from constants.messages import ARE_YOU_SURE_OF_UPLOADING_THIS_MEDIA
from constants.messages import CAPTION_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM
from constants.messages import FILE_IS_NOT_VALID
from constants.messages import MEDIA_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM
from constants.messages import MESSAGE_FOR_GET_LOGIN_DATA
from constants.messages import PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN
from constants.messages import (
    SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
)
from constants.messages import SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM
from constants.messages import SOMETHING_WENT_WRONG
from constants.messages import UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO
from constants.messages import WHAT_DO_YOU_WANT
from constants.messages import WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM
from constants.messages import YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM
from constants.states import HOME_STATE
from constants.states import LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE
from constants.states import LOGIN_WITH_TWO_FACTOR_AUTHENTICATION
from constants.states import LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD
from constants.states import SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT
from constants.states import SET_MEDIA_AND_GET_CAPTION
from constants.states import SET_MEDIA_TYPE_AND_GET_MEDIA
from constants.states import VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from core.keyboards import media_type_keyboard
from core.keyboards import yes_or_no_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)

CLIENT = Client()
CLIENT.delay_range = [1, 3]
CAPTION = None
MEDIA_TYPE = None
USER_UPLOADED_FILE_TYPE = None
FILE_PATH_ON_SERVER = None
USERNAME = None
PASSWORD = None


@send_action(ChatAction.TYPING)
async def get_login_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    time.sleep(5)
    await update.message.reply_text(
        MESSAGE_FOR_GET_LOGIN_DATA, reply_markup=back_keyboard
    )
    return LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE


@send_action(ChatAction.TYPING)
async def login_attempt_and_get_media_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    time.sleep(3)
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    username, password = message.split("\n")
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    user_instagram_session = f"{login_directory}/{username}_{user_id}.json"
    user_instagram_session_is_exist = os.path.exists(user_instagram_session)
    if user_instagram_session_is_exist:
        CLIENT.load_settings(user_instagram_session)
        CLIENT.login(username, password)
        try:
            CLIENT.get_timeline_feed()
            await update.effective_user.send_message(
                WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
                reply_markup=media_type_keyboard,
            )
            return SET_MEDIA_TYPE_AND_GET_MEDIA
        except LoginRequired:
            os.remove(user_instagram_session)
            CLIENT.login(username, password)
            CLIENT.dump_settings(
                f"{login_directory}/{username}_{user_id}.json")
            await update.effective_user.send_message(
                WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
                reply_markup=media_type_keyboard,
            )
            return SET_MEDIA_TYPE_AND_GET_MEDIA
        except ClientError as error:
            if PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN in error.message:
                await update.effective_user.send_message(
                    PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN,
                    reply_markup=base_keyboard,
                )
                return HOME_STATE
    try:
        CLIENT.login(username, password)
        CLIENT.dump_settings(f"{login_directory}/{username}_{user_id}.json")
    except TwoFactorRequired:
        global USERNAME
        global PASSWORD
        USERNAME = username
        PASSWORD = password
        await update.effective_user.send_message(
            "Please Send Two Factor Authentication Code", reply_markup=back_keyboard
        )
        return LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD
    await update.effective_user.send_message(
        WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
        reply_markup=media_type_keyboard,
    )
    return SET_MEDIA_TYPE_AND_GET_MEDIA


@send_action(ChatAction.TYPING)
async def login_with_two_factor_authentication(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""

    time.sleep(5)
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    code = message
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"

    CLIENT.login(username=USERNAME, password=PASSWORD, verification_code=code)
    CLIENT.dump_settings(f"{login_directory}/{USERNAME}_{user_id}.json")

    await update.effective_user.send_message(
        WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
        reply_markup=media_type_keyboard,
    )
    return SET_MEDIA_TYPE_AND_GET_MEDIA


@send_action(ChatAction.TYPING)
async def set_media_type_and_get_media(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    message = update.message
    global MEDIA_TYPE
    if message.text == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    elif message.text == UPLOAD_PHOTO_KEY:
        MEDIA_TYPE = PHOTO
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    elif message.text == UPLOAD_VIDEO_KEY:
        MEDIA_TYPE = VIDEO
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    elif message.text == UPLOAD_ALBUM_KEY:
        MEDIA_TYPE = ALBUM
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    elif message.text == UPLOAD_REELS_KEY:
        MEDIA_TYPE = REEL
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    elif message.text == UPLOAD_IGTV_KEY:
        MEDIA_TYPE = IGTV
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    else:
        await update.effective_user.send_message(
            "media type is not valid, please try again",
            reply_markup=base_keyboard,
        )


@send_action(ChatAction.TYPING)
async def set_media_and_get_caption(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    global USER_UPLOADED_FILE_TYPE
    global FILE_PATH_ON_SERVER
    message = update.message
    if message.text == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    elif update.message.document:
        media = await update.message.document.get_file()
        USER_UPLOADED_FILE_TYPE = constants.DOCUMENT
    elif update.message.video:
        media = await update.message.video.get_file()
        USER_UPLOADED_FILE_TYPE = constants.VIDEO
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        media = await context.bot.get_file(file_id)
        USER_UPLOADED_FILE_TYPE = constants.PHOTO
    else:
        await update.message.reply_text(FILE_IS_NOT_VALID, reply_markup=base_keyboard)
        return HOME_STATE

    current_directory = os.getcwd()
    download_directory = f"{current_directory}/download"
    download_directory_is_exist = os.path.exists(download_directory)
    if not download_directory_is_exist:
        os.makedirs(download_directory)
    file_path = await media.download_to_drive()
    FILE_PATH_ON_SERVER = str(file_path)
    await update.effective_user.send_message(
        SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
        reply_markup=back_keyboard,
    )
    return SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT


@send_action(ChatAction.TYPING)
async def set_caption_and_asking_to_confirm_the_content(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    global CAPTION
    CAPTION = update.message.text
    await update.effective_user.send_message(
        MEDIA_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM
    )
    if USER_UPLOADED_FILE_TYPE == constants.PHOTO:
        await update.effective_user.send_photo(photo=FILE_PATH_ON_SERVER)

    elif USER_UPLOADED_FILE_TYPE == constants.VIDEO:
        await update.effective_user.send_video(video=FILE_PATH_ON_SERVER)

    elif USER_UPLOADED_FILE_TYPE == constants.DOCUMENT:
        await update.effective_user.send_document(document=FILE_PATH_ON_SERVER)
    await update.effective_user.send_message(
        CAPTION_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM
    )
    await update.effective_user.send_message(CAPTION)
    await update.effective_user.send_message(
        ARE_YOU_SURE_OF_UPLOADING_THIS_MEDIA,
        reply_markup=yes_or_no_keyboard,
    )
    return VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM


@send_action(ChatAction.TYPING)
async def verify_content_and_upload_on_instagram(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message != YES:
        os.remove(FILE_PATH_ON_SERVER)
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    try:
        if MEDIA_TYPE == PHOTO:
            await update.effective_user.send_message(PROCESSING)
            try:
                media_object = CLIENT.photo_upload(
                    path=FILE_PATH_ON_SERVER, caption=CAPTION
                )
                media_url = f"https://instagram.com/p/{media_object.code}"
                os.remove(FILE_PATH_ON_SERVER)
                await update.effective_user.send_message(
                    YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                        media_url=media_url
                    ),
                    reply_markup=base_keyboard,
                )
                return HOME_STATE
            except UnknownError as error:
                if error.message in UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO:
                    await update.effective_user.send_message(
                        f"{UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO}, Please try again",
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
        if MEDIA_TYPE == VIDEO:
            await update.effective_user.send_message(PROCESSING)
            media_object = CLIENT.video_upload(
                path=FILE_PATH_ON_SERVER, caption=CAPTION
            )
            media_url = f"https://instagram.com/reel/{media_object.code}"
            os.remove(FILE_PATH_ON_SERVER)
            await update.effective_user.send_message(
                YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                    media_url=media_url
                ),
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        if MEDIA_TYPE == IGTV:
            return HOME_STATE
        if MEDIA_TYPE == REEL:
            await update.effective_user.send_message(PROCESSING)
            media_object = CLIENT.clip_upload(
                path=FILE_PATH_ON_SERVER, caption=CAPTION)
            media_url = f"https://instagram.com/reel/{media_object.code}"
            os.remove(FILE_PATH_ON_SERVER)
            await update.effective_user.send_message(
                YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                    media_url=media_url
                ),
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        if MEDIA_TYPE == ALBUM:
            return HOME_STATE
    except (PhotoNotUpload, IGTVNotUpload, ClipNotUpload, VideoNotUpload):
        await update.effective_user.send_message(
            f"{SOMETHING_WENT_WRONG}, {PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN}",
            reply_markup=base_keyboard,
        )
