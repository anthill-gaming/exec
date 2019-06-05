from anthill.platform.api.internal import connector
from functools import partial
from .base import session_api


def market_request():
    return partial(connector.internal_request, 'market')


@session_api()
async def list_items(market_id, filters=None):
    pass


@session_api()
async def list_orders(market_id, filters=None):
    pass


@session_api()
async def list_sellers(market_id):
    pass


@session_api()
async def beckome_seller(market_id):
    pass


@session_api()
async def check_seller(market_id):
    pass


@session_api()
async def create_item(market_id):
    pass


@session_api()
async def remove_item(item_id):
    pass


@session_api()
async def purchase_item(item_id):
    pass
