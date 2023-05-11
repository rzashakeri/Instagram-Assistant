import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]
NAME = os.environ["NAME"]
ADMIN_TELEGRAM_USER_ID = int(os.environ["ADMIN_TELEGRAM_USER_ID"])
POSTGRESQL_HOST = os.environ["POSTGRESQL_HOST"]
POSTGRESQL_PORT = os.environ["POSTGRESQL_PORT"]
POSTGRESQL_NAME = os.environ["POSTGRESQL_NAME"]
POSTGRESQL_USERNAME = os.environ["POSTGRESQL_USERNAME"]
POSTGRESQL_PASSWORD = os.environ["POSTGRESQL_PASSWORD"]
IS_MAINTENANCE = bool(os.environ["IS_MAINTENANCE"])
LIST_OF_ADMINS = [ADMIN_TELEGRAM_USER_ID]
WEBHOOK = False
# The following configuration is only needed if you setted WEBHOOK to True #
WEBHOOK_OPTIONS = {
    "listen": "0.0.0.0",  # IP
    "port": 443,
    "url_path": TOKEN,  # This is recommended for avoiding random people
    # making fake updates to your bot
    "webhook_url": f"https://example.com/{TOKEN}",
}
