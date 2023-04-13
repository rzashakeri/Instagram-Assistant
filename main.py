from telegram.ext import Application

from configurations import settings
from core.handlers import base_conversation_handler
from utils import create_requirement_folders, logger

if __name__ == "__main__":
    logger.init_logger(f"logs/{settings.NAME}.log")
    create_requirement_folders()
    application = (
        Application.builder()
        .token(settings.TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .get_updates_read_timeout(42)
        .build()
    )
    conversation_handler = base_conversation_handler()
    application.add_handler(conversation_handler)
    application.run_polling()
