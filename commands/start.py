# encoding: utf-8
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

from connectors.postgresql import create_request
from connectors.postgresql import create_user
from constants import NO
from constants.messages import GOODBYE_WE_ARE_SORRY
from constants.messages import WELCOME_MESSAGE
from constants.request_types import FEEDBACK_REQUEST
from constants.request_types import START_REQUEST
from constants.states import HOME_STATE
from core.keyboards import base_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    message = update.message.text
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username
    if message == NO:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=GOODBYE_WE_ARE_SORRY.format(first_name=first_name),
        )
        return ConversationHandler.END
    create_user(user_id, first_name, last_name, username)
    create_request(user_id=user_id, request_type=FEEDBACK_REQUEST)
    await update.message.reply_text(
        WELCOME_MESSAGE.format(first_name=first_name),
        reply_markup=base_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    return HOME_STATE
