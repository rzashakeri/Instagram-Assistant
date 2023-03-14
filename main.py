from telegram.ext import Application
from configurations import settings
from utils import logger
from bot.conversation import conversation

if __name__ == "__main__":
    logger.init_logger(f"logs/{settings.NAME}.log")
    application = Application.builder().token(settings.TOKEN).build()
    conversation_handler = conversation()
    application.add_handler(conversation_handler)
    application.run_polling()
