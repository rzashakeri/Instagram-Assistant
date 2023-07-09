import os
from logging import getLogger

from instagrapi import Client
from instagrapi.exceptions import BadPassword
from instagrapi.exceptions import ChallengeError
from instagrapi.exceptions import ChallengeRequired
from instagrapi.exceptions import ClientError
from instagrapi.exceptions import ClientForbiddenError
from instagrapi.exceptions import FeedbackRequired
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import PleaseWaitFewMinutes
from instagrapi.exceptions import PrivateError
from instagrapi.exceptions import RateLimitError
from instagrapi.exceptions import RecaptchaChallengeForm
from instagrapi.exceptions import ReloginAttemptExceeded
from instagrapi.exceptions import SelectContactPointRecoveryForm
from requests.exceptions import ProxyError

from core.exceptions import LoginException
from utils import next_proxy

logger = getLogger(__name__)


class CustomClient:
    """custom client"""

    def __init__(self,
                 username: str,
                 password: str,
                 verification_code: str = ""):
        self.username = username
        self.password = password
        self.verification_code = verification_code

    def get_client(
        self,
        login_directory,
        telegram_user_id,
        user_instagram_session="",
        save_session=False,
    ):
        """We return the client class, in which we automatically handle exceptions
        You can move the "handle_exception" above or into an external module"""

        def handle_exception(client, error):
            last_json = client.last_json
            logger.info(last_json)

            if last_json != {}:
                try:
                    if last_json.get("challenge_type_enum_str",
                                     "") == "HACKED_LOCK":
                        logger.info("raises 'HACKED_LOCK' error in last_json")
                        logger.info(last_json)
                        raise LoginException({
                            "status": "fail",
                            "message": "HACKED_LOCK"
                        })
                    elif (last_json.get("challenge_type_enum_str",
                                        "") == "SCRAPING_WARNING"):
                        logger.info(
                            "raises 'SCRAPING_WARNING' error in last_json")
                        logger.info(last_json)
                        raise LoginException({
                            "status": "fail",
                            "message": "SCRAPING_WARNING"
                        })
                    elif last_json.get("message", "") == "user_has_logged_out":
                        logger.info(
                            "raises 'user_has_logged_out' error in last_json")
                        logger.info(last_json)
                        raise LoginException({
                            "status": "fail",
                            "message": "user_has_logged_out"
                        })
                    elif (last_json.get("message", "") ==
                          "Please wait a few minutes before you try again."):
                        logger.info(
                            "raises 'Please wait a few minutes before you try again.' error in last_json"
                        )
                        logger.info(last_json)
                        raise LoginException({
                            "status":
                            "fail",
                            "message":
                            "please_wait_a_few_minutes"
                        })
                    elif (last_json.get("payload", "").get(
                            "message", ""
                    ) == "We're sorry, but something went wrong. Please try again."
                          ):
                        logger.info(
                            "raises 'We're sorry, but something went wrong. Please try again.' error in last_json"
                        )
                        logger.info(last_json)
                        raise LoginException({
                            "status":
                            "fail",
                            "message":
                            "we_re_sorry_but_something_went_wrong_please_try_again",
                        })
                    elif last_json.get("challenge", "").get(
                            "api_path", "") == "/challenge/" or last_json.get(
                                "step_name", ""):
                        logger.info(
                            "raises 'challenge_required' error in last_json")
                        logger.info(last_json)
                        raise LoginException({
                            "status": "fail",
                            "message": "challenge_required"
                        })
                    elif (last_json.get(
                            "message", ""
                    ) == "Instagram has blocked your IP address, use a quality proxy provider (not free, not shared)"
                          ):
                        logger.info(
                            "raises 'Instagram has blocked your IP address, use a quality proxy provider (not free, not shared)' error from last_json"
                        )
                        logger.info(error)
                        client.set_proxy(next_proxy())
                        raise LoginException({
                            "status": "fail",
                            "message": error
                        })
                except AttributeError:
                    pass

            if isinstance(error, BadPassword):
                logger.info("raises 'BadPassword' error")
                logger.info(error)
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, RateLimitError):
                logger.info("raises 'RateLimitError' error")
                logger.info(error)
                client.set_proxy(next_proxy())
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, LoginRequired):
                logger.info("raises 'LoginRequired' error")
                logger.info(error)
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ChallengeRequired):
                logger.info("raises 'ChallengeRequired' error")
                logger.info(error)
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, FeedbackRequired):
                logger.info("raises 'FeedbackRequired' error")
                logger.info(error)
                message = client.last_json["feedback_message"]
                if ("This action was blocked. Please try again later"
                        in message or
                        "We restrict certain activity to protect our community"
                        in message
                        or "Your account has been temporarily blocked"
                        in message):
                    raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, PleaseWaitFewMinutes):
                logger.info("raises 'PleaseWaitFewMinutes' error")
                logger.info(error)
                client.set_proxy(next_proxy())
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ClientForbiddenError):
                logger.info("raises 'ClientForbiddenError' error")
                logger.info(error)
                client.set_proxy(next_proxy())
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ChallengeError):
                logger.info("raises 'ChallengeError' error")
                logger.info(error)
                raise LoginException({"status": "fail", "message": error})
            elif isinstance(error, ProxyError):
                logger.info("raises 'ProxyError' error")
                logger.info(error)
                client.set_proxy(next_proxy())
                raise LoginException({"status": "fail", "message": error})
            raise error

        client = Client(proxy=next_proxy(), request_timeout=7)
        logger.info("proxy is %s", client.proxy)
        client.delay_range = [1, 3]
        client.handle_exception = handle_exception
        user_instagram_session_is_exist = os.path.exists(
            user_instagram_session)
        if user_instagram_session_is_exist:
            client.load_settings(user_instagram_session)
            client.login(username=self.username, password=self.password)
            client.get_timeline_feed()
        elif self.verification_code != "" and save_session:
            if save_session:
                client.login(
                    username=self.username,
                    password=self.password,
                    verification_code=self.verification_code,
                )
                client.dump_settings(
                    f"{login_directory}/{self.username}_{telegram_user_id}.json"
                )
            client.login(
                username=self.username,
                password=self.password,
                verification_code=self.verification_code,
            )
        else:
            if save_session:
                client.login(username=self.username, password=self.password)
                client.dump_settings(
                    f"{login_directory}/{self.username}_{telegram_user_id}.json"
                )
            client.login(username=self.username, password=self.password)
        return client
