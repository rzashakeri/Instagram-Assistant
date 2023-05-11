# encoding: utf-8
import time
from datetime import datetime, timezone
from logging import getLogger

import psycopg2
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from configurations.settings import ADMIN_TELEGRAM_USER_ID
from connectors.postgresql import create_user
from constants import NO, YES
from constants.keys import BACK_KEY
from constants.messages import (FEEDBACK_MESSAGE, GOODBYE_WE_ARE_SORRY,
                                NEW_MESSAGE, NEW_TEXT_MESSAGE, PRIVACY_MESSAGE,
                                WELCOME_MESSAGE, WHAT_DO_YOU_WANT,
                                YOUR_MESSAGE_WAS_SENT)
from constants.states import FEEDBACK_STATE, HOME_STATE
from core.keyboards import back_keyboard, base_keyboard
from utils.decorators import send_action

# Init logger

logger = getLogger(__name__)


@send_action(ChatAction.TYPING)
async def get_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=FEEDBACK_MESSAGE,
        reply_markup=back_keyboard,
    )
    return FEEDBACK_STATE


@send_action(ChatAction.TYPING)
async def send_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    # pylint: disable=unused-argument
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username

    text_message = update.message.text
    video_message = update.message.video
    audio_message = update.message.audio
    voice_message = update.message.voice
    photo_message = update.message.photo
    document_message = update.message.document

    if update.message.text == BACK_KEY:
        await update.message.reply_text(WHAT_DO_YOU_WANT, reply_markup=base_keyboard)
        return HOME_STATE

    if text_message is not None:
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_USER_ID,
            text=NEW_TEXT_MESSAGE.format(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                message=update.message.text,
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif video_message is not None:
        await context.bot.send_video(
            chat_id=ADMIN_TELEGRAM_USER_ID,
            video=update.message.video,
        )
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_USER_ID,
            text=NEW_TEXT_MESSAGE.format(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                message=update.message.text,
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif audio_message is not None:
        await context.bot.send_audio(
            chat_id=ADMIN_TELEGRAM_USER_ID, audio=update.message.audio
        )
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_USER_ID,
            text=NEW_TEXT_MESSAGE.format(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                message=update.message.text,
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif voice_message is not None:
        await context.bot.send_audio(
            chat_id=ADMIN_TELEGRAM_USER_ID, audio=voice_message
        )
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_USER_ID,
            text=NEW_TEXT_MESSAGE.format(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                message=update.message.text,
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif photo_message is not None:
        photo_id = update.message.photo[-1].file_id
        photo = await context.bot.get_file(photo_id)
        await context.bot.photo(chat_id=ADMIN_TELEGRAM_USER_ID, photo=photo)
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_USER_ID,
            text=NEW_TEXT_MESSAGE.format(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                message=update.message.text,
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif document_message is not None:
        await context.bot.document(
            chat_id=ADMIN_TELEGRAM_USER_ID, document=update.message.document
        )
        await context.bot.send_message(
            chat_id=ADMIN_TELEGRAM_USER_ID,
            text=NEW_TEXT_MESSAGE.format(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                message=update.message.text,
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    else:
        await update.message.reply_text(
            "Your Message Not Valid, Please Try Again", reply_markup=back_keyboard
        )
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=YOUR_MESSAGE_WAS_SENT,
        reply_markup=base_keyboard,
    )
    return HOME_STATE
