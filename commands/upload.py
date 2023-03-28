# encoding: utf-8
import os
import constants
from logging import getLogger

from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ClientError,
    PhotoNotUpload,
    IGTVNotUpload,
    ClipNotUpload,
    VideoNotUpload,
    UnknownError,
)
from telegram import Update
from telegram.ext import ContextTypes

from constants import BACK, LOGIN, YES, PROCESSING, DOCUMENT
from constants.keyboards import (
    UPLOAD_REELS_KEY,
    UPLOAD_PHOTO_KEY,
    UPLOAD_VIDEO_KEY,
    UPLOAD_ALBUM_KEY,
    UPLOAD_IGTV_KEY,
)
from constants.media_types import REEL, PHOTO, VIDEO, ALBUM, IGTV
from constants.messages import (
    MESSAGE_FOR_GET_LOGIN_DATA,
    WHAT_DO_YOU_WANT,
    SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
    WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
    SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
    ARE_YOU_SURE_OF_UPLOADING_THIS_MEDIA,
    MEDIA_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM,
    CAPTION_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM,
    YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM,
    SOMETHING_WENT_WRONG,
    FILE_IS_NOT_VALID,
    UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO,
    PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN,
)
from constants.states import (
    HOME_STATE,
    LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE,
    SET_MEDIA_TYPE_AND_GET_MEDIA,
    SET_MEDIA_AND_GET_CAPTION,
    SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT,
    VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM,
)
from core.keyboards import (
    base_keyboard,
    back_keyboard,
    media_type_keyboard,
    yes_or_no_keyboard,
)

# Init logger
logger = getLogger(__name__)

CLIENT = Client()
CAPTION = None
MEDIA_TYPE = None
USER_UPLOADED_FILE_TYPE = None
FILE_PATH_ON_SERVER = None


async def get_login_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    await update.message.reply_text(
        MESSAGE_FOR_GET_LOGIN_DATA, reply_markup=back_keyboard
    )
    return LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE


async def login_attempt_and_get_media_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message == BACK:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    username, password = message.split("\n")
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    user_instagram_session = f"{login_directory}/{username}_{user_id}.json"
    login_directory_is_exist = os.path.isdir(login_directory)
    user_instagram_session_is_exist = os.path.exists(user_instagram_session)
    if not login_directory_is_exist:
        os.makedirs(login_directory)
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
            CLIENT.dump_settings(f"{login_directory}/{username}_{user_id}.json")
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
    CLIENT.login(username, password)
    CLIENT.dump_settings(f"{login_directory}/{username}_{user_id}.json")
    instagram_api_response = CLIENT.last_json
    challenge_type = instagram_api_response.get("challenge_type_enum_str")
    if challenge_type == "HACKED_LOCK":
        await update.effective_user.send_message(
            "challenge required, Please try again later",
            reply_markup=media_type_keyboard,
        )
        return HOME_STATE
    await update.effective_user.send_message(
        WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
        reply_markup=media_type_keyboard,
    )
    return SET_MEDIA_TYPE_AND_GET_MEDIA


async def set_media_type_and_get_media(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    message = update.message
    global MEDIA_TYPE
    if message.text == BACK:
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


async def set_media_and_get_caption(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    global USER_UPLOADED_FILE_TYPE
    global FILE_PATH_ON_SERVER
    message = update.message
    if message.text == BACK:
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


async def set_caption_and_asking_to_confirm_the_content(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    message = update.message.text
    if message == BACK:
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
            media_object = CLIENT.clip_upload(path=FILE_PATH_ON_SERVER, caption=CAPTION)
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
