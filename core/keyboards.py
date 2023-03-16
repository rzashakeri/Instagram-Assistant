from telegram import ReplyKeyboardMarkup

from core.constants import DOWNLOAD_MEDIA, UPLOAD_MEDIA, INSIGHT, LOGIN, BACK_TO_HOME, BACK, DOWNLOAD, UPLOAD

base_reply_keyboard: list = [
    [DOWNLOAD, UPLOAD],
    [INSIGHT],
    [LOGIN],
]
base_keyboard = ReplyKeyboardMarkup(base_reply_keyboard, resize_keyboard=True)

back_reply_keyboard = [[BACK]]
back_keyboard = ReplyKeyboardMarkup(back_reply_keyboard, resize_keyboard=True)
