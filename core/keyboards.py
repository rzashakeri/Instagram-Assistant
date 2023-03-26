from telegram import ReplyKeyboardMarkup

from constants.keyboards import DOWNLOAD_KEY, UPLOAD_KEY, INSIGHT_KEY, LOGIN_KEY, BACK_KEY, UPLOAD_REELS_KEY, UPLOAD_PHOTO_KEY, UPLOAD_VIDEO_KEY, UPLOAD_ALBUM_KEY, UPLOAD_IGTV_KEY

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
