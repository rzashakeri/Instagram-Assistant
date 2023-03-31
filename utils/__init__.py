from functools import wraps

from configurations.settings import LIST_OF_ADMINS


def restricted(func):
    """This decorator allows you to restrict the access of a handler to only the user_ids specified in LIST_OF_ADMINS."""
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
