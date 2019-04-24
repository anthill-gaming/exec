from anthill.platform.api.internal import connector
from functools import partial
from .base import session_api


event_request = partial(connector.internal_request, 'event')
