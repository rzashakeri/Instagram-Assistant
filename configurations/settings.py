import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.environ['TOKEN']
NAME = os.environ['NAME']
INSTAGRAM_USERNAME = os.environ['INSTAGRAM_USERNAME']
INSTAGRAM_PASSWORD = os.environ['INSTAGRAM_PASSWORD']
TELEGRAM_USER_ID = int(os.environ['TELEGRAM_USER_ID'])
POSTGRESQL_HOST = os.environ['POSTGRESQL_HOST']
POSTGRESQL_PORT = os.environ['POSTGRESQL_PORT']
POSTGRESQL_NAME = os.environ['POSTGRESQL_NAME']
POSTGRESQL_USERNAME = os.environ['POSTGRESQL_USERNAME']
POSTGRESQL_PASSWORD = os.environ['POSTGRESQL_PASSWORD']
LIST_OF_ADMINS = [TELEGRAM_USER_ID]
WEBHOOK = False
# The following configuration is only needed if you setted WEBHOOK to True #
WEBHOOK_OPTIONS = {
    "listen": "0.0.0.0",  # IP
    "port": 443,
    "url_path": TOKEN,  # This is recommended for avoiding random people
    # making fake updates to your bot
    "webhook_url": f"https://example.com/{TOKEN}",
}
