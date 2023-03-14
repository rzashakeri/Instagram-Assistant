from telegram import ReplyKeyboardMarkup

from constants import DOWNLOAD_MEDIA, UPLOAD_MEDIA, INSIGHT, LOGIN

main_reply_keyboard: list = [
    [DOWNLOAD_MEDIA],
    [UPLOAD_MEDIA],
    [INSIGHT],
    [LOGIN],
]
main_keyboard = ReplyKeyboardMarkup(main_reply_keyboard)
