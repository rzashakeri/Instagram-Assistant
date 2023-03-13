from telegram.ext import ConversationHandler, CommandHandler

from bot.start import start
from constants import CHOOSING, TYPING_REPLY, TYPING_CHOICE

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [],
        TYPING_CHOICE: [],
        TYPING_REPLY: [],
    },
    fallbacks=[],
)
