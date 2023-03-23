from telegram import ReplyKeyboardMarkup

from constants.keyboards import DOWNLOAD_KEY, UPLOAD_KEY, INSIGHT_KEY, LOGIN_KEY, BACK_KEY

base_reply_keyboard: list = [
    [DOWNLOAD_KEY, UPLOAD_KEY],
    [INSIGHT_KEY],
    [LOGIN_KEY],
]
base_keyboard = ReplyKeyboardMarkup(base_reply_keyboard, resize_keyboard=True)

back_reply_keyboard = [[BACK_KEY]]
back_keyboard = ReplyKeyboardMarkup(back_reply_keyboard, resize_keyboard=True)
