import datetime, pytz
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import filters
from telegram.ext import MessageHandler
from telegram.ext import PicklePersistence

from commands.maintenance import maintenance
from commands.admin import admin, get_insight
from configurations import settings
from configurations.settings import IS_MAINTENANCE, ADMIN_TELEGRAM_USER_ID
from core.handlers import base_conversation_handler, admin_conversation_handler
from utils import create_requirement_folders
from utils import logger
from utils.logger import clear_logs_file_daily

if __name__ == "__main__":
    logger.init_logger(f"logs/{settings.NAME}.log")
    create_requirement_folders()
    persistence = PicklePersistence(filepath="conversation states")
    application = (Application.builder().token(
        settings.TOKEN).read_timeout(50).write_timeout(
        50).get_updates_read_timeout(50).persistence(persistence).build())
    if IS_MAINTENANCE:
        application.add_handler(CommandHandler("start", maintenance))
        application.add_handler(admin_conversation_handler())
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, maintenance))
    else:
        application.add_handler(base_conversation_handler())
        application.job_queue.run_daily(
            callback=clear_logs_file_daily,
            time=datetime.time(hour=0, minute=0, tzinfo=pytz.timezone('Asia/Tehran')),
            days=(0, 1, 2, 3, 4, 5, 6)
        )
        application.job_queue.run_daily(
            callback=get_insight,
            time=datetime.time(hour=0, minute=0, tzinfo=pytz.timezone('Asia/Tehran')),
            days=(0, 1, 2, 3, 4, 5, 6),
            chat_id=ADMIN_TELEGRAM_USER_ID
        )
    application.run_polling()
