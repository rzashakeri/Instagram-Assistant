# encoding: utf-8

from logging import getLogger

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher

from core.keyboards import main_keyboard
from core.constants import CHOOSING

# Init logger
logger = getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler("start", start))


def start(update: Update, _: CallbackContext):
    """Process a /start command."""
    welcome_message: str = """
    Hi, Welcome To Instagram in Telegram Bot, With this robot you can do whatever you do on Instagram using the telegram with additional features.
    """
    update.message.reply_text(text=welcome_message, reply_markup=main_keyboard)
    return CHOOSING
