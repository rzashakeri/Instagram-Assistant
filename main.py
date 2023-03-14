from telegram.ext import Application
from configurations import settings
from utils import logger
from core.handlers import base_conversation_handler

if __name__ == "__main__":
    logger.init_logger(f"logs/{settings.NAME}.log")
    application = Application.builder().token(settings.TOKEN).build()
    conversation_handler = base_conversation_handler()
    application.add_handler(conversation_handler)
    application.run_polling()
