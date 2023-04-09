# encoding: utf-8
from logging import getLogger
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from connectors.postgresql import create_user
from constants.messages import WELCOME_MESSAGE, PRIVACY_MESSAGE
from constants.states import HOME_STATE
from core.keyboards import base_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def lottery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    pass
