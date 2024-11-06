
"""Create Read Update Delete."""
from .valid_customers import Customer


def create_user(user_in: Customer):  # noqa
    user = user_in.model_dump()
    return {
        'status': 'success',
        'user': user,
    }
