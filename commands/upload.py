# encoding: utf-8
import os
import time
from logging import getLogger

from instagrapi.exceptions import ClientError
from instagrapi.exceptions import ClipNotUpload
from instagrapi.exceptions import IGTVNotUpload
from instagrapi.exceptions import PhotoNotUpload
from instagrapi.exceptions import PrivateError
from instagrapi.exceptions import TwoFactorRequired
from instagrapi.exceptions import UnknownError
from instagrapi.exceptions import VideoNotUpload
from telegram import Update
from telegram.constants import ChatAction
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import constants
from connectors.postgresql import create_request
from constants import LOGIN
from constants import NO
from constants import PROCESSING
from constants import YES
from constants.keys import BACK_KEY
from constants.keys import UPLOAD_ALBUM_KEY
from constants.keys import UPLOAD_IGTV_KEY
from constants.keys import UPLOAD_PHOTO_KEY
from constants.keys import UPLOAD_REELS_KEY
from constants.keys import UPLOAD_STORY_KEY
from constants.keys import UPLOAD_VIDEO_KEY
from constants.media_types import ALBUM
from constants.media_types import IGTV
from constants.media_types import PHOTO
from constants.media_types import REEL
from constants.media_types import STORY
from constants.media_types import VIDEO
from constants.messages import ARE_YOU_SURE_OF_UPLOADING_THIS_MEDIA
from constants.messages import CAPTION_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM
from constants.messages import FILE_IS_NOT_VALID
from constants.messages import INSTAGRAM_ASSISTANT_ID
from constants.messages import MEDIA_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM
from constants.messages import MESSAGE_FOR_GET_LOGIN_DATA
from constants.messages import PLEASE_SEND_PHOTO_OR_VIDEO
from constants.messages import PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN
from constants.messages import REMEMBER_ME
from constants.messages import (
    SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
)
from constants.messages import SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM
from constants.messages import SEND_ME_THE_TITLE_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM
from constants.messages import SOMETHING_WENT_WRONG
from constants.messages import TITLE_OF_YOUR_IGTV
from constants.messages import UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO
from constants.messages import WHAT_DO_YOU_WANT
from constants.messages import WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM
from constants.messages import YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM
from constants.request_types import RULE_REQUEST, UPLOAD_REQUEST
from constants.states import HOME_STATE
from constants.states import IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN
from constants.states import (
    IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN_IN_UPLOAD,
)
from constants.states import LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE
from constants.states import LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD
from constants.states import SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT
from constants.states import SET_MEDIA_AND_GET_CAPTION
from constants.states import SET_MEDIA_TYPE_AND_GET_MEDIA
from constants.states import SET_TITLE_OF_IGTV_AND_GET_CAPTION
from constants.states import VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM
from core.exceptions import LoginException
from core.instagram import CustomClient
from core.keyboards import back_keyboard
from core.keyboards import base_keyboard
from core.keyboards import media_type_keyboard
from core.keyboards import yes_or_no_keyboard
from utils import remove_all_spaces
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)

CLIENT = None
CAPTION = None
MEDIA_TYPE = None
MEDIA_MIME = None
USER_UPLOADED_FILE_TYPE = None
FILE_PATH_ON_SERVER = None
USERNAME = None
PASSWORD = None
IGTV_TITLE = None
IS_IGTV = False
IS_REEL = False
IS_VIDEO = False


@send_action(ChatAction.TYPING)
async def get_login_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    await update.message.reply_text(
        MESSAGE_FOR_GET_LOGIN_DATA.format(
            instagram_assistant_id=INSTAGRAM_ASSISTANT_ID
        ),
        reply_markup=back_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    return IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN_IN_UPLOAD


@send_action(ChatAction.TYPING)
async def remember_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    logger.info("Is your session saved for the next login?")
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    try:
        global USERNAME
        global PASSWORD
        username, password = message.split("\n")
        USERNAME = remove_all_spaces(username).lower()
        PASSWORD = remove_all_spaces(password)
    except ValueError:
        await update.message.reply_text(
            MESSAGE_FOR_GET_LOGIN_DATA,
            reply_markup=back_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
        return IS_YOUR_LOGIN_INFORMATION_SAVED_FOR_THE_NEXT_LOGIN
    await update.message.reply_text(
        "⚠️ Attention: This robot saves a session for next Login if you want",
        reply_markup=back_keyboard,
    )
    await update.message.reply_text(REMEMBER_ME, reply_markup=yes_or_no_keyboard)
    return LOGIN_ATTEMPT_AND_GET_MEDIA_TYPE


@send_action(ChatAction.TYPING)
async def login_attempt_and_get_media_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    time.sleep(3)
    logger.info("login attempt")
    message = update.message.text
    if message == BACK_KEY:
        logger.info("back to home")
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    user_instagram_session = f"{login_directory}/{USERNAME}_{user_id}.json"
    global CLIENT
    try:
        CLIENT = CustomClient(username=USERNAME, password=PASSWORD).get_client(
            login_directory=login_directory,
            telegram_user_id=user_id,
            user_instagram_session=user_instagram_session,
        )
        global SAVED_LOGIN_INFORMATION
        if message == YES:
            logger.info("Saved session")
            SAVED_LOGIN_INFORMATION = True
            CLIENT = CustomClient(username=USERNAME, password=PASSWORD).get_client(
                login_directory=login_directory,
                telegram_user_id=user_id,
                user_instagram_session=user_instagram_session,
                save_session=True,
            )
        else:
            logger.info("not Save session")
            SAVED_LOGIN_INFORMATION = False
            CLIENT = CustomClient(username=USERNAME, password=PASSWORD).get_client(
                login_directory=login_directory,
                telegram_user_id=user_id,
                user_instagram_session=user_instagram_session,
                save_session=True,
            )
        await update.effective_user.send_message(
            WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=media_type_keyboard,
        )
        try:
            create_request(
                user_id=update.effective_user.id, request_type=UPLOAD_REQUEST
            )
            logger.info("create upload request successfully")
        except Exception as error:
            logger.info(error)
            logger.info("create upload request failed")
        return SET_MEDIA_TYPE_AND_GET_MEDIA
    except TwoFactorRequired:
        logger.info("Get Two Factor Authentication Code")
        await update.effective_user.send_message(
            "Please Send Two Factor Authentication Code", reply_markup=back_keyboard
        )
        return LOGIN_WITH_TWO_FACTOR_AUTHENTICATION_FOR_UPLOAD
    except (LoginException, ClientError, PrivateError):
        await update.effective_user.send_message(
            SOMETHING_WENT_WRONG,
            reply_markup=base_keyboard,
        )
        return HOME_STATE


@send_action(ChatAction.TYPING)
async def login_with_two_factor_authentication(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    logger.info("Login With Two Factor Authentication Code")
    time.sleep(5)
    message = update.message.text
    if message == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    user_id = update.effective_user.id
    current_directory = os.getcwd()
    verification_code = remove_all_spaces(message)
    current_directory = os.getcwd()
    login_directory = f"{current_directory}/{LOGIN.lower()}"
    global SAVED_LOGIN_INFORMATION
    global CLIENT
    try:
        if SAVED_LOGIN_INFORMATION:
            CLIENT = CustomClient(
                username=USERNAME,
                password=PASSWORD,
                verification_code=verification_code,
            ).get_client(
                login_directory=login_directory,
                telegram_user_id=user_id,
                save_session=True,
            )
        CLIENT = CustomClient(
            username=USERNAME, password=PASSWORD, verification_code=verification_code
        ).get_client(
            login_directory=login_directory,
            telegram_user_id=user_id,
            save_session=False,
        )
        await update.effective_user.send_message(
            WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=media_type_keyboard,
        )
        try:
            create_request(
                user_id=update.effective_user.id, request_type=UPLOAD_REQUEST
            )
            logger.info("create upload request successfully")
        except Exception as error:
            logger.info(error)
            logger.info("create upload request failed")
        return SET_MEDIA_TYPE_AND_GET_MEDIA
    except (LoginException, ClientError, PrivateError):
        await update.effective_user.send_message(
            SOMETHING_WENT_WRONG,
            reply_markup=base_keyboard,
        )
        return HOME_STATE


@send_action(ChatAction.TYPING)
async def set_media_type_and_get_media(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    message = update.message
    global MEDIA_TYPE
    global IS_IGTV
    global IS_REEL
    global IS_VIDEO
    if message.text == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    elif message.text == UPLOAD_STORY_KEY:
        MEDIA_TYPE = STORY
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    elif message.text == UPLOAD_PHOTO_KEY:
        MEDIA_TYPE = PHOTO
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    elif message.text == UPLOAD_VIDEO_KEY:
        MEDIA_TYPE = VIDEO
        IS_VIDEO = True
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
        IS_REEL = True
        await update.effective_user.send_message(
            SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_MEDIA_AND_GET_CAPTION
    elif message.text == UPLOAD_IGTV_KEY:
        MEDIA_TYPE = IGTV
        IS_IGTV = True
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
    global MEDIA_MIME
    message = update.message
    if message.text == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    elif update.message.document:
        media = await update.message.document.get_file()
        USER_UPLOADED_FILE_TYPE = constants.DOCUMENT
        MEDIA_MIME = update.message.document.mime_type
    elif update.message.video:
        media = await update.message.video.get_file()
        USER_UPLOADED_FILE_TYPE = constants.VIDEO
        MEDIA_MIME = update.message.video.mime_type
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        media = await context.bot.get_file(file_id)
        USER_UPLOADED_FILE_TYPE = constants.PHOTO
        MEDIA_MIME = constants.JPEG_MIME
    else:
        await update.message.reply_text(FILE_IS_NOT_VALID, reply_markup=base_keyboard)
        return HOME_STATE
    logger.info("starting download media ...")
    file_path = await media.download_to_drive()
    logger.info("download completed")
    FILE_PATH_ON_SERVER = str(file_path)
    if MEDIA_TYPE == STORY:
        await update.effective_user.send_message(
            MEDIA_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM
        )
        if USER_UPLOADED_FILE_TYPE == constants.PHOTO:
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=ChatAction.UPLOAD_PHOTO,
            )
            await update.effective_user.send_photo(photo=FILE_PATH_ON_SERVER)

        elif USER_UPLOADED_FILE_TYPE == constants.VIDEO:
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=ChatAction.UPLOAD_VIDEO,
            )
            await update.effective_user.send_video(video=FILE_PATH_ON_SERVER)

        elif USER_UPLOADED_FILE_TYPE == constants.DOCUMENT:
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=ChatAction.UPLOAD_DOCUMENT,
            )
            await update.effective_user.send_document(document=FILE_PATH_ON_SERVER)
        await update.effective_user.send_message(
            ARE_YOU_SURE_OF_UPLOADING_THIS_MEDIA,
            reply_markup=yes_or_no_keyboard,
        )
        return VERIFY_CONTENT_AND_UPLOAD_ON_INSTAGRAM
    if MEDIA_TYPE == IGTV and IS_IGTV:
        await update.effective_user.send_message(
            SEND_ME_THE_TITLE_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
            reply_markup=back_keyboard,
        )
        return SET_TITLE_OF_IGTV_AND_GET_CAPTION
    await update.effective_user.send_message(
        SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM,
        reply_markup=back_keyboard,
    )
    return SET_CAPTION_AND_ASKING_TO_CONFIRM_THE_CONTENT


@send_action(ChatAction.TYPING)
async def set_title_of_igtv_and_get_caption(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    # pylint: disable=unused-argument
    """Select an action: Adding parent/child or show data."""
    if update.message.text == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE
    global IGTV_TITLE
    IGTV_TITLE = update.message.text
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
    global IGTV_TITLE
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
    if IGTV_TITLE is not None:
        await update.effective_user.send_message(TITLE_OF_YOUR_IGTV)
        await update.effective_user.send_message(IGTV_TITLE)
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

    if message == BACK_KEY:
        os.remove(FILE_PATH_ON_SERVER)
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE

    if message == NO:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        os.remove(FILE_PATH_ON_SERVER)
        return HOME_STATE
    try:
        if MEDIA_TYPE == STORY:
            processing_message = await context.bot.send_message(
                chat_id=update.message.chat_id, text=PROCESSING
            )
            try:
                if MEDIA_MIME == constants.JPEG_MIME:
                    story_object = CLIENT.photo_upload_to_story(
                        path=FILE_PATH_ON_SERVER
                    )
                    media_url = f"https://instagram.com/stories/{story_object.user.username}/{story_object.id}"
                    os.remove(FILE_PATH_ON_SERVER)
                    await context.bot.deleteMessage(
                        message_id=processing_message.message_id,
                        chat_id=update.message.chat_id,
                    )
                    await update.effective_user.send_message(
                        YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                            media_url=media_url,
                            instagram_assistant_id=INSTAGRAM_ASSISTANT_ID,
                        ),
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
                elif MEDIA_MIME == "mp4":
                    story_object = CLIENT.video_upload_to_story(
                        path=FILE_PATH_ON_SERVER
                    )
                    media_url = f"https://instagram.com/stories/{story_object.user.username}/{story_object.id}"
                    os.remove(FILE_PATH_ON_SERVER)
                    await context.bot.deleteMessage(
                        message_id=processing_message.message_id,
                        chat_id=update.message.chat_id,
                    )
                    await update.effective_user.send_message(
                        YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                            media_url=media_url,
                            instagram_assistant_id=INSTAGRAM_ASSISTANT_ID,
                        ),
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
                else:
                    await update.effective_user.send_message(
                        PLEASE_SEND_PHOTO_OR_VIDEO,
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
            except UnknownError as error:
                os.remove(FILE_PATH_ON_SERVER)
                if error.message in UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO:
                    await update.effective_user.send_message(
                        f"{UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO}, Please try again",
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
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
                        media_url=media_url,
                        instagram_assistant_id=INSTAGRAM_ASSISTANT_ID,
                    ),
                    reply_markup=base_keyboard,
                )
                return HOME_STATE
            except UnknownError as error:
                os.remove(FILE_PATH_ON_SERVER)
                if error.message in UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO:
                    await update.effective_user.send_message(
                        f"{UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO}, Please try again",
                        reply_markup=base_keyboard,
                    )
                    return HOME_STATE
        if MEDIA_TYPE == VIDEO and IS_VIDEO:
            await update.effective_user.send_message(PROCESSING)
            media_object = CLIENT.video_upload(
                path=FILE_PATH_ON_SERVER, caption=CAPTION
            )
            media_url = f"https://instagram.com/reel/{media_object.code}"
            os.remove(FILE_PATH_ON_SERVER)
            await update.effective_user.send_message(
                YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                    media_url=media_url, instagram_assistant_id=INSTAGRAM_ASSISTANT_ID
                ),
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        if MEDIA_TYPE == IGTV and IS_IGTV:
            await update.effective_user.send_message(PROCESSING)
            media_object = CLIENT.igtv_upload(
                path=FILE_PATH_ON_SERVER, caption=CAPTION, title=""
            )
            media_url = f"https://instagram.com/p/{media_object.code}"
            os.remove(FILE_PATH_ON_SERVER)
            await update.effective_user.send_message(
                YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                    media_url=media_url, instagram_assistant_id=INSTAGRAM_ASSISTANT_ID
                ),
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        if MEDIA_TYPE == REEL and IS_REEL:
            await update.effective_user.send_message(PROCESSING)
            media_object = CLIENT.clip_upload(path=FILE_PATH_ON_SERVER, caption=CAPTION)
            media_url = f"https://instagram.com/reel/{media_object.code}"
            os.remove(FILE_PATH_ON_SERVER)
            os.remove(f"{FILE_PATH_ON_SERVER}.jpg")
            await update.effective_user.send_message(
                YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM.format(
                    media_url=media_url, instagram_assistant_id=INSTAGRAM_ASSISTANT_ID
                ),
                reply_markup=base_keyboard,
            )
            return HOME_STATE
        if MEDIA_TYPE == ALBUM:
            return HOME_STATE
    except (PhotoNotUpload, IGTVNotUpload, ClipNotUpload, VideoNotUpload):
        os.remove(FILE_PATH_ON_SERVER)
        await update.effective_user.send_message(
            f"{SOMETHING_WENT_WRONG}, {PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN}",
            reply_markup=base_keyboard,
        )
        return HOME_STATE
