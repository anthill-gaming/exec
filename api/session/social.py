from anthill.platform.api.internal import connector
from functools import partial
from . import session_api


social_request = partial(connector.internal_request, 'social')
