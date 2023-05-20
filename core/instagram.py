import os

from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    RecaptchaChallengeForm,
    ReloginAttemptExceeded,
    SelectContactPointRecoveryForm,
    RateLimitError,
    ClientForbiddenError,
    ClientError,
    PrivateError,
    ChallengeError,
)

from core.exceptions import LoginException


class CustomClient:
    """custom client"""
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def get_client(
        self, save_session, login_directory, telegram_user_id, user_instagram_session
    ):
        """We return the client class, in which we automatically handle exceptions
        You can move the "handle_exception" above or into an external module"""
        
        def handle_exception(client, error):
            last_json = client.last_json
            if last_json["challenge_type_enum_str"] == "HACKED_LOCK":
                raise LoginException({"status": "fail", "message": "HACKED_LOCK"})
            elif last_json["challenge_type_enum_str"] == "SCRAPING_WARNING":
                raise LoginException({"status": "fail", "message": "SCRAPING_WARNING"})
            elif last_json["message"] == "user_has_logged_out":
                raise LoginException(
                    {"status": "fail", "message": "user_has_logged_out"}
                )
            elif (
                last_json["payload"]["message"]
                == "We're sorry, but something went wrong. Please try again."
            ):
                raise LoginException(
                    {
                        "status": "fail",
                        "message": "we_re_sorry_but_something_went_wrong_please_try_again",
                    }
                )
            elif last_json["challenge"]["api_path"] == "/challenge/" or last_json.get(
                "step_name", ""
            ):
                raise LoginException(
                    {"status": "fail", "message": "challenge_required"}
                )

            if isinstance(error, BadPassword):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, RateLimitError):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, LoginRequired):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ChallengeRequired):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, FeedbackRequired):
                message = client.last_json["feedback_message"]
                if (
                    "This action was blocked. Please try again later" in message
                    or "We restrict certain activity to protect our community"
                    in message
                    or "Your account has been temporarily blocked" in message
                ):
                    raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, PleaseWaitFewMinutes):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ClientForbiddenError):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ClientError):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, PrivateError):
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ChallengeError):
                raise LoginException({"status": "fail", "message": error})
            raise error

        client = Client()
        client.handle_exception = handle_exception
        user_instagram_session_is_exist = os.path.exists(user_instagram_session)
        if user_instagram_session_is_exist:
            client.load_settings(user_instagram_session)
            client.login(self.username, self.password)
            client.get_timeline_feed()
        if save_session:
            client.login(self.username, self.password)
            client.dump_settings(
                f"{login_directory}/{self.username}_{telegram_user_id}.json"
            )
        client.login(self.username, self.password)
        return client