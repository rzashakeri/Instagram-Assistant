# encoding: utf-8
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from constants.messages import PRIVACY_MESSAGE
from constants.messages import RULE_MESSAGE
from constants.states import START_STATE
from core.keyboards import yes_or_no_without_back_key
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def rule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    first_name = update.effective_user.first_name
    await context.bot.send_message(chat_id=update.message.chat_id, text="⚠️")
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=RULE_MESSAGE.format(rule_message=PRIVACY_MESSAGE,
                                 first_name=first_name),
        reply_markup=yes_or_no_without_back_key,
    )
    return START_STATE
