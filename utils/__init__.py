import os
import time
from abc import abstractmethod
from collections import defaultdict

from telegram.ext import BaseRateLimiter
from telegram.ext import CommandHandler
from telegram.ext import Updater

from constants import LOGIN


class CustomRateLimiter(BaseRateLimiter):

    async def initialize(self) -> None:
        """Initialize resources used by this class. Must be implemented by a subclass."""

    async def shutdown(self) -> None:
        """Stop & clear resources used by this class. Must be implemented by a subclass."""

    def __init__(self, max_requests, time_interval):
        super().__init__()
        self.max_requests = max_requests
        self.time_interval = time_interval
        self.user_requests = defaultdict(list)

    async def process_request(self, callback, *args, **kwargs):
        user_id = kwargs.get("chat_id") or kwargs.get("user_id")
        if user_id is not None and not self.check_limit(user_id):
            # Return None if rate limit is exceeded
            return ValueError("rate limit is exceeded")

        return await callback(*args, **kwargs)  # Proceed with the request

    def check_limit(self, user_id):
        current_time = time.time()
        user_times = self.user_requests[user_id]
        user_times.append(current_time)

        while user_times and user_times[0] < current_time - self.time_interval:
            user_times.pop(0)

        return len(user_times) <= self.max_requests


def create_requirement_folders():
    """create requirement folders"""
    current_directory = os.getcwd()

    download_directory = f"{current_directory}/download"
    download_directory_is_exist = os.path.exists(download_directory)
    if not download_directory_is_exist:
        os.makedirs(download_directory)

    login_directory = f"{current_directory}/{LOGIN.lower()}"
    login_directory_is_exist = os.path.exists(login_directory)
    if not login_directory_is_exist:
        os.makedirs(login_directory)


def remove_all_spaces(string):
    return "".join(string.split())
