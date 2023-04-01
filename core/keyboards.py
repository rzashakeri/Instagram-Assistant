from telegram import ReplyKeyboardMarkup

from constants import YES, NO, EMAIL, PHONE
from constants.keys import DOWNLOAD_KEY, UPLOAD_KEY, INSIGHT_KEY, LOGIN_KEY, BACK_KEY, UPLOAD_REELS_KEY, UPLOAD_PHOTO_KEY, UPLOAD_VIDEO_KEY, UPLOAD_ALBUM_KEY, UPLOAD_IGTV_KEY, BACK_TO_HOME_KEY

base_reply_keyboard: list = [
    [DOWNLOAD_KEY, UPLOAD_KEY],
    [INSIGHT_KEY],
    [LOGIN_KEY],
]
base_keyboard = ReplyKeyboardMarkup(base_reply_keyboard, resize_keyboard=True)

back_reply_keyboard = [[BACK_KEY]]
back_keyboard = ReplyKeyboardMarkup(back_reply_keyboard, resize_keyboard=True)

media_type_reply_keyboard = [
    [UPLOAD_REELS_KEY],
    [UPLOAD_PHOTO_KEY],
    [UPLOAD_VIDEO_KEY],
    [UPLOAD_ALBUM_KEY],
    [UPLOAD_IGTV_KEY],
]
media_type_keyboard = ReplyKeyboardMarkup(media_type_reply_keyboard, resize_keyboard=True)

yes_or_no_reply_keyboard = [
    [NO], [YES]
]
yes_or_no_keyboard = ReplyKeyboardMarkup(yes_or_no_reply_keyboard, resize_keyboard=True)


email_or_phone_reply_keyboard = [
    [EMAIL],
    [PHONE]
]
email_or_phone_keyboard = ReplyKeyboardMarkup(email_or_phone_reply_keyboard, resize_keyboard=True)

admin_reply_keyboard = [
    [BACK_TO_HOME_KEY]
]
admin_keyboard = ReplyKeyboardMarkup(admin_reply_keyboard, resize_keyboard=True)
