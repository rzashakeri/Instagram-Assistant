from instagrapi.mixins.challenge import ChallengeChoice


def get_code_from_sms(username):
    pass


def get_code_from_email(username):
    pass


def challenge_code_handler(username, choice):
    """Handles challenge"""
    if choice == ChallengeChoice.SMS:
        return get_code_from_sms(username)

    elif choice == ChallengeChoice.EMAIL:
        return get_code_from_email(username)
    return False
