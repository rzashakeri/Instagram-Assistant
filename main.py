import datetime

import pytz
import sentry_sdk
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import filters
from telegram.ext import MessageHandler
from telegram.ext import PicklePersistence
from telegram.ext import AIORateLimiter

from commands.admin import admin
from commands.admin import daily_insight
from commands.maintenance import maintenance
from configurations import settings
from configurations.settings import ADMIN_TELEGRAM_USER_ID
from configurations.settings import IS_MAINTENANCE
from configurations.settings import SENTRY_DSN
from core.handlers import admin_conversation_handler
from core.handlers import base_conversation_handler
from utils import create_requirement_folders
from utils.logger import init_logger
from utils.logger import clear_logs_file_daily
from logging import getLogger

logger = getLogger(__name__)

if __name__ == "__main__":
    init_logger(f"logs/{settings.NAME}.log")
    logger.info("Instagram Assistant has been started")
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )
    create_requirement_folders()
    persistence = PicklePersistence(filepath="conversation states")
    application = (
        Application.builder()
        .token(settings.TOKEN)
        .concurrent_updates(True)
        .read_timeout(50)
        .write_timeout(50)
        .get_updates_read_timeout(50)
        .persistence(persistence)
        .rate_limiter(AIORateLimiter())
        .build()
    )
    application.job_queue.run_daily(
        callback=clear_logs_file_daily,
        time=datetime.time(hour=0, minute=0, tzinfo=pytz.timezone("Asia/Tehran")),
        days=(0, 1, 2, 3, 4, 5, 6),
    )
    application.job_queue.run_daily(
        callback=daily_insight,
        time=datetime.time(hour=0, minute=0, tzinfo=pytz.timezone("Asia/Tehran")),
        days=(0, 1, 2, 3, 4, 5, 6),
    )
    if IS_MAINTENANCE:
        application.add_handler(CommandHandler("start", maintenance))
        application.add_handler(admin_conversation_handler())
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, maintenance)
        )
    else:
        application.add_handler(base_conversation_handler())
    application.run_polling()
