from anthill.platform.api.internal import connector
from functools import partial
from .base import session_api


promo_request = partial(connector.internal_request, 'promo')
