from anthill.platform.api.internal import connector
from functools import partial
from .base import session_api


game_request = partial(connector.internal_request, 'game_master')
