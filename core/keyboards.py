from telegram import ReplyKeyboardMarkup

from core.constants import DOWNLOAD_MEDIA, UPLOAD_MEDIA, INSIGHT, LOGIN, BACK

base_reply_keyboard: list = [
    [DOWNLOAD_MEDIA, UPLOAD_MEDIA],
    [INSIGHT],
    [LOGIN],
]
base_keyboard = ReplyKeyboardMarkup(base_reply_keyboard)

back_reply_keyboard: list = [[BACK]]
back_keyboard = ReplyKeyboardMarkup(back_reply_keyboard)
