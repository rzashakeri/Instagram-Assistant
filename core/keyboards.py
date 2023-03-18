from telegram import ReplyKeyboardMarkup

from core.constants import DOWNLOAD_MEDIA, UPLOAD_MEDIA, INSIGHT, LOGIN, BACK_TO_HOME, BACK, DOWNLOAD, UPLOAD, WHAT_DO_YOU_WANT, HOME

base_reply_keyboard: list = [
    [DOWNLOAD, UPLOAD],
    [INSIGHT],
    [LOGIN],
]
base_keyboard = ReplyKeyboardMarkup(base_reply_keyboard, resize_keyboard=True)

back_reply_keyboard = [[BACK]]
back_keyboard = ReplyKeyboardMarkup(back_reply_keyboard, resize_keyboard=True)


async def back_action(message, update):
    if message == BACK:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME
