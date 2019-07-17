from anthill.platform.api.internal import connector
from functools import partial
from .base import session_api


def profile_request():
    return partial(connector.internal_request, 'profile')
