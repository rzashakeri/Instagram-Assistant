import os

from constants import LOGIN


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
