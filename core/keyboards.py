from telegram import ReplyKeyboardMarkup

from constants import EMAIL
from constants import NO
from constants import PHONE
from constants import YES
from constants.keys import BACK_KEY
from constants.keys import BACK_TO_HOME_KEY
from constants.keys import DOWNLOAD_KEY
from constants.keys import INSIGHT_KEY
from constants.keys import LOGIN_KEY
from constants.keys import LOTTERY_KEY
from constants.keys import LOTTERY_WITH_COMMENTS_LIST
from constants.keys import LOTTERY_WITH_LIKES_LIST
from constants.keys import PRIVACY_KEY
from constants.keys import SEND_MESSAGE_TO_ALL_USER_KEY
from constants.keys import UPLOAD_ALBUM_KEY
from constants.keys import UPLOAD_IGTV_KEY
from constants.keys import UPLOAD_KEY
from constants.keys import UPLOAD_PHOTO_KEY
from constants.keys import UPLOAD_REELS_KEY
from constants.keys import UPLOAD_VIDEO_KEY
from constants.keys import USER_COUNT_KEY

base_reply_keyboard: list = [
    [DOWNLOAD_KEY, UPLOAD_KEY],
    [INSIGHT_KEY, PRIVACY_KEY],
    [LOTTERY_KEY, LOGIN_KEY],
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
media_type_keyboard = ReplyKeyboardMarkup(media_type_reply_keyboard,
                                          resize_keyboard=True)

yes_or_no_reply_keyboard = [[NO], [YES]]
yes_or_no_keyboard = ReplyKeyboardMarkup(yes_or_no_reply_keyboard,
                                         resize_keyboard=True)

email_or_phone_reply_keyboard = [[EMAIL], [PHONE]]
email_or_phone_keyboard = ReplyKeyboardMarkup(email_or_phone_reply_keyboard,
                                              resize_keyboard=True)

admin_reply_keyboard = [
    [SEND_MESSAGE_TO_ALL_USER_KEY, USER_COUNT_KEY],
    [BACK_TO_HOME_KEY],
]
admin_keyboard = ReplyKeyboardMarkup(admin_reply_keyboard,
                                     resize_keyboard=True)

lottery_reply_keyboard = [
    [LOTTERY_WITH_LIKES_LIST],
    [LOTTERY_WITH_COMMENTS_LIST],
    [BACK_KEY],
]
lottery_keyboard = ReplyKeyboardMarkup(lottery_reply_keyboard,
                                       resize_keyboard=True)
