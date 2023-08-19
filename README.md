[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Instagram Assistant

[Instagram Assistant](https://t.me/InstagramAssistantRobot) in telegram with extra feature 💡

## Features

1. Download Any Media From Instagram Such Reels, Profile Photo And etc...
2. Upload Any Type Of Media From Telegram in Instagram (**Login Required**)
3. Received Insights Of Instagram Post from Telegram
4. Lottery with comments and likes
5. Getting User Info

### when you run as admin

6. Admin Panel
7. Get User Count From Admin Panel
8. Send Message To All User From Admin Panel

## Why was this robot created?

I live in Iran and because of the intense filtering,
it is easier to use telegram with proxy and more
accessible, and I thought I could use the telegram
when I couldn't access Instagram to upload my own
content into my [Instagram page](https://www.instagram.com/barnamenevisiinsta).
So I also made this robot Open Source for those
friends who love to run this robot on their
personal server and can use it or do not trust
the [robot](https://t.me/InstagramAssistantRobot) for any reason.

## How Deploy?

1 . first clone this repository :

`git clone https://github.com/rzashakeri/Instagram-Assistant.git`

2 . go to `Instagram-Assistant` directory :

`cd Instagram-Assistant`

3 . Create a Virtual Environment :

`python -m venv venv`

4 . activated the virtual environment :

`source venv/bin/activate`

5 . now install dependencies:

`pip install -r requirements.txt`

6 . create .env file and set environment variables :

`vim .env` or `nano .env`

7 . set your environment variables such `.env.example`

| key                      | description                                         |
| ------------------------ | --------------------------------------------------- |
| `TOKEN`                  | Your Bot Token                                      |
| `NAME`                   | Your Bot Name                                       |
| `ADMIN_TELEGRAM_USER_ID` | Your User Id                                        |
| `POSTGRESQL_HOST`        | Your postgresql database host such `123.456.678.9`  |
| `POSTGRESQL_PORT`        | Your postgresql database port such `1234`           |
| `POSTGRESQL_NAME`        | Your postgresql database name such `my_bot_db`      |
| `POSTGRESQL_USERNAME`    | Your postgresql database user name such `root`      |
| `POSTGRESQL_PASSWORD`    | Your postgresql database password such `xxxxx`      |
| `IS_MAINTENANCE`         | This shows that your robot is in maintenance or not |
| `SENTRY_DSN`             | Your sentry dsn                                     |

8 . create a file with name `admin_users.json` :

`vim admin_users.json`

9 . Here you need to enter the username and passwords
of the accounts you already created and the robot can
be used them and perform various operations such
as download and lottery.

The contents of the file (`admin_users.json`) should be as follows:

```json
{
  "users": [
    {
      "username": "testuser1",
      "password": "password"
    },
    {
      "username": "testuser2",
      "password": "password"
    },
    {
      "username": "testuser3",
      "password": "password"
    }
  ]
}
```

10 . run bot with this command :

```
python supervisor.py
```

**DONE ✅**

## Stack

1. python
2. [python-telegram-bot](https://python-telegram-bot.org/)
3. [instagrapi](https://github.com/adw0rd/instagrapi)
4. PostgreSQL
