# encoding: utf-8
import time
from datetime import datetime, timezone
from logging import getLogger

import psycopg2
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from connectors.postgresql import create_user
from constants import NO, YES
from constants.keys import BACK_KEY
from constants.messages import (GOODBYE_WE_ARE_SORRY, PRIVACY_MESSAGE,
                                WELCOME_MESSAGE)
from constants.states import HOME_STATE
from core.keyboards import base_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def get_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    pass
