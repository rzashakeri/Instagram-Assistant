DOWNLOAD_MEDIA: str = "Download Media"
UPLOAD_MEDIA: str = "Upload Media"
LOGIN_TO_INSTAGRAM: str = "Login To Instagram"
INSIGHT_OF_POST: str = "Insights"
BACK: str = "Back"
MESSAGE_FOR_GET_LOGIN_DATA: str = (
    "Please send me login information in the following format and format: \n"
    "\n"
    "username\n"
    "password"
)
WHAT_DO_YOU_WANT: str = "what do you want ?"
YOU_WERE_ALREADY_LOGGED_IN: str = "You Were Already Logged In"
LOGGED_IN_SUCCESSFULLY: str = "Logged In Successfully"
DOWNLOAD_COMPLETED: str = "Download Complete"
LINK_IS_INVALID: str = "Link is Invalid, check your Link and Try Again"
STARTING_DOWNLOAD: str = "Starting Download ..."
UPLOAD_IN_TELEGRAM: str = "Upload In Telegram ..."
IS_VIDEO: str = "video"
WELCOME_MESSAGE: str = (
    "Hi {first_name}, Welcome To Instagram in Telegram Bot, "
    "With this robot you can do whatever you do "
    "on Instagram using the telegram with additional features."
)

# Media Types
PHOTO: int = 1
VIDEO: int = 2
IGTV: int = 2
REEL: int = 2
ALBUM: int = 8

# Product Types
IS_FEED: str = "feed"
IS_IGTV: str = "igtv"
IS_CLIPS: str = "clips"

(  # states
    HOME,
    DOWNLOAD,
    UPLOAD,
    LOGIN
) = range(4)

(
    INSIGHT,
    BACK_ACTION,
    BACK_TO_HOME,
) = range(4, 7)
