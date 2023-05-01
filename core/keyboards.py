from telegram import ReplyKeyboardMarkup

from constants import YES, NO, EMAIL, PHONE
from constants.keys import (
    DOWNLOAD_KEY,
    UPLOAD_KEY,
    INSIGHT_KEY,
    BACK_KEY,
    UPLOAD_REELS_KEY,
    UPLOAD_PHOTO_KEY,
    UPLOAD_VIDEO_KEY,
    UPLOAD_ALBUM_KEY,
    UPLOAD_IGTV_KEY,
    BACK_TO_HOME_KEY,
    SEND_MESSAGE_TO_ALL_USER_KEY,
    USER_COUNT_KEY,
    PRIVACY_KEY,
    LOTTERY_WITH_COMMENTS_LIST,
    LOTTERY_WITH_LIKES_LIST,
    LOTTERY_KEY,
    UPLOAD_STORY_KEY,
)

base_reply_keyboard: list = [
    [DOWNLOAD_KEY, UPLOAD_KEY],
    [INSIGHT_KEY, LOTTERY_KEY],
    [PRIVACY_KEY],
]
base_keyboard = ReplyKeyboardMarkup(base_reply_keyboard, resize_keyboard=True)

back_reply_keyboard = [[BACK_KEY]]
back_keyboard = ReplyKeyboardMarkup(back_reply_keyboard, resize_keyboard=True)

media_type_reply_keyboard = [
    [UPLOAD_STORY_KEY],
    [UPLOAD_REELS_KEY],
    [UPLOAD_PHOTO_KEY],
    [UPLOAD_VIDEO_KEY],
    [UPLOAD_ALBUM_KEY],
    [UPLOAD_IGTV_KEY],
]
media_type_keyboard = ReplyKeyboardMarkup(
    media_type_reply_keyboard, resize_keyboard=True
)

yes_or_no_reply_keyboard = [[NO, YES], [BACK_KEY]]
yes_or_no_keyboard = ReplyKeyboardMarkup(yes_or_no_reply_keyboard, resize_keyboard=True)

yes_or_no_without_back_key_reply_keyboard = [
    [NO, YES],
]
yes_or_no_without_back_key = ReplyKeyboardMarkup(
    yes_or_no_without_back_key_reply_keyboard, resize_keyboard=True
)

email_or_phone_reply_keyboard = [[EMAIL], [PHONE]]
email_or_phone_keyboard = ReplyKeyboardMarkup(
    email_or_phone_reply_keyboard, resize_keyboard=True
)

admin_reply_keyboard = [
    [SEND_MESSAGE_TO_ALL_USER_KEY, USER_COUNT_KEY],
    [BACK_TO_HOME_KEY],
]
admin_keyboard = ReplyKeyboardMarkup(admin_reply_keyboard, resize_keyboard=True)

lottery_reply_keyboard = [
    [LOTTERY_WITH_LIKES_LIST],
    [LOTTERY_WITH_COMMENTS_LIST],
    [BACK_KEY],
]
lottery_keyboard = ReplyKeyboardMarkup(lottery_reply_keyboard, resize_keyboard=True)
