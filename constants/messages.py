MESSAGE_FOR_GET_LOGIN_DATA: str = (
    "Please send me login information in the following format and format: \n"
    "\n"
    "username\n"
    "password\n"
    "\n"
    "*we don,t save your username and Password* \n"
    "Next step if you want to save the session on our servers\n"
    "\n"
    "*what is session ?* \n"
    "when you use your mobile device, you login to Instagram once and then you "
    "can use it for a long time without logging in again. This is because "
    "Instagram stores your session on your device and you can use it to "
    "login to Instagram without entering your username and password again.")
WHAT_DO_YOU_WANT: str = "what do you want ?"
YOU_WERE_ALREADY_LOGGED_IN: str = "You Were Already Logged In"
LOGGED_IN_SUCCESSFULLY: str = "Logged In Successfully"
DOWNLOAD_COMPLETED: str = "Download Complete"
LINK_IS_INVALID: str = "Link is Invalid, check your Link and Try Again"
STARTING_DOWNLOAD: str = "Starting Download ..."
UPLOAD_IN_TELEGRAM: str = "Upload In Telegram ..."
IS_VIDEO: str = "video"
WELCOME_MESSAGE: str = (
    "Hi {first_name}, Welcome To Instagram Assistant Bot, "
    "With this robot you can do whatever you do "
    "on Instagram using the telegram with additional features.\n"
    "\n"
    "Why should we use this robot?\n"
    "1. Download Any Media From Instagram Such Reels, Profile Photo And etc...\n"
    "2. Upload Any Type Of Media From Telegram in Instagram\n"
    "3. Received Insights Of Instagram Post from Telegram\n"
    "4. Lottery based on likes and comments.\n"
    "5. All features are free\n"
    "6. [Open Source](https://github.com/rzashakeri/Instagram-Assistant) \n"
    "7. There is no compulsory membership\n")
SEND_ME_THE_MEDIA_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM: str = (
    "Send me the media you want to upload on Instagram")
SEND_ME_THE_CAPTION_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM: str = (
    "Send me the caption of post you want to upload on Instagram")
SEND_ME_THE_TITLE_OF_POST_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM: str = (
    "Send me the title of IGTV you want to upload on Instagram")
WHAT_TYPE_OF_CONTENT_DO_YOU_WANT_TO_UPLOAD_ON_INSTAGRAM: str = (
    f"{LOGGED_IN_SUCCESSFULLY} What type of content do you want to upload on Instagram"
)
ARE_YOU_SURE_OF_UPLOADING_THIS_MEDIA: str = "Are you sure of uploading this media?"
MEDIA_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM: str = (
    "Media that is going to be uploaded to Instagram")
TITLE_OF_YOUR_IGTV: str = "Title Of Your IGTV"
CAPTION_THAT_IS_GOING_TO_BE_UPLOADED_TO_INSTAGRAM: str = (
    "Caption that is going to be uploaded to Instagram")
YOUR_CONTENT_IS_SUCCESSFULLY_UPLOADED_TO_INSTAGRAM: str = (
    "Your content is successfully uploaded to Instagram and you can "
    "access it with the following link:\n"
    "{media_url}")
UPLOAD_WAS_CANCELED_BY_THE_USER: str = "Upload was canceled by the user"
SOMETHING_WENT_WRONG: str = "Something Went Wrong"
FILE_IS_NOT_VALID: str = "File is not valid, You must be uploaded image or video"
OK_SEND_ME_THE_LINK_YOU_WANT_TO_DOWNLOAD: str = "OK, send me the link you want to download from Instagram Such Profile, Post, Story and etc... or for Download Profile Picture Send Username With @ Such @Username"
SEND_THE_POST_LINK_YOU_WANT_TO_GET_THE_STATISTICS: str = "Send the post link you want to get the statistics or send instagram username such @username for getting user info"
PLEASE_WAIT_A_FEW_MINUTES_BEFORE_YOU_TRY_AGAIN: str = (
    "Please wait a few minutes before you try again")
UPLOADED_IMAGE_ISNT_IN_AN_ALLOWED_ASPECT_RATIO: str = (
    "Uploaded image isn't in an allowed aspect ratio")
INSIGHT_OF_MEDIA: str = ("Post statistics:\n"
                         "Like Count: {like_count}\n"
                         "Comment Count: {comment_count}\n"
                         "Save Count: {save_count}\n"
                         "Share Count: {share_count}")
WELCOME_TO_ADMIN: str = "Welcome To Admin, What are you doing?"
USER_COUNT: str = "User Count: {user_count}"
WELCOME_TO_HOME: str = "Welcome To Home, What are you doing?"
SEND_YOUR_MESSAGE: str = "Send Your Message 👇"
YOUR_MESSAGE_WAS_SENT: str = "Your Message Was Sent"
PRIVACY_MESSAGE: str = (
    "⚠️ This robot stores the following telegram information:\n"
    "User ID,First Name, Last Name, Username\n"
    "\n"
    "And when you login Instagram through this robot for upload media, if you want to save the session for the next login on our servers\n"
    "\n"
    "You can change your password after you log in via the robot "
    "and erase the relevant session through the original Instagram app\n"
    "\n"
    "Source Code: https://github.com/rzashakeri/Instagram-Assistant")
WELCOME_TO_THE_LOTTERY_SECTION: str = (
    "Welcome to the lottery section, Send the post link for lottery 👇")
WELL_YOU_WANT_TO_DO_THE_LOTTERY_ON_WHAT_BASIS: str = (
    "Well you want to do the lottery on what basis:")
REMEMBER_ME: str = "Is your login information saved for the next login?"
USER_NOT_FOUND_CHECK_USERNAME_AND_TRY_AGAIN: str = (
    "User not found, check username and try again")
PLEASE_SEND_PHOTO_OR_VIDEO: str = "file is not valid, please send a photo (Support JPG files) or video (Support MP4 files)"
GETTING_STORY_INFORMATION: str = "Getting Story information ..."
GETTING_MEDIA_INFORMATION: str = "Getting media information ..."
GETTING_PROFILE_INFORMATION: str = "Getting profile information ..."
THIS_ROBOT_SAVES_A_SESSION_FOR_NEXT_LOGIN_IF_YOU_WANT: str = (
    "⚠️ Attention: This robot saves a session for next Login if you want")
BOT_UNDER_MAINTENANCE: str = "Bot Under Maintenance 🛠️\nThank you for waiting"
MEDIA_NOT_FOUND: str = (
    "Media Not Found or Unavailable, Please Check Your Link And Try Again")
RULE_MESSAGE: str = """
Hi {first_name}, To work with the robot you must first read the following rules and then you can work with the robot\n
{rule_message}\n
\n
Do you accept the privacy laws of this robot?
"""
GOODBYE_WE_ARE_SORRY: str = (
    "Goodbye, we are sorry that we couldn't create a good experience for you")
SENDING_THUMBNAIL: str = "Sending thumbnail ..."
SENDING_VIDEO: str = "Sending Video ..."
USER_INFO: str = """
{username} Info:\n
Full Name: {full_name}\n
Biography:\n {biography}\n
Following: {following}\n
Follower: {follower}\n
Media Count: {media_count}
"""
INSTAGRAM_COM: str = "instagram.com"
PLEASE_SEND_THE_INSTAGRAM_LINK: str = "Link is Invalid, Please Send The Instagram Link With Domain instagram.com and Try Again"
FEEDBACK_MESSAGE: str = (
    "Welcome To Feedback Section\n"
    "You can send us any comments or criticisms or suggestions")
NEW_MESSAGE: str = (
    "Have a new message From [{first_name}](tg://user?id={user_id}) \n"
    "User Information:\n}"
    "User ID: {user_id}"
    "first name: {first_name}\n"
    "last name: {last_name}\n"
    "username: @{username}\n")
NEW_TEXT_MESSAGE: str = (
    "Have a new message From [{first_name}](tg://user?id={user_id}) \n"
    "Message: {message} \n"
    "User Information:\n"
    "User ID: {user_id}\n"
    "first name: {first_name}\n"
    "last name: {last_name}\n"
    "username: @{username}\n")
YOUR_MESSAGE_WAS_SENT: str = "your message was sent\nThank For Submit Feedback 🙏"
