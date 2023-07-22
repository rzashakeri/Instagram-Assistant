# encoding: utf-8
from logging import getLogger

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from connectors.postgresql import create_request
from constants.messages import PRIVACY_MESSAGE
from constants.request_types import LOTTERY_REQUEST
from constants.request_types import PRIVACY_REQUEST
from constants.states import HOME_STATE
from core.keyboards import base_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await update.message.reply_text(
        PRIVACY_MESSAGE,
        reply_markup=base_keyboard,
    )
    try:
        create_request(user_id=update.effective_user.id, request_type=PRIVACY_REQUEST)
        logger.info("create privacy request successfully")
    except Exception as error:
        logger.info(error)
        logger.info("create privacy request failed")
    return HOME_STATE
