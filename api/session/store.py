from anthill.platform.api.internal import connector
from functools import partial
from . import session_api


store_request = partial(connector.internal_request, 'store')


@session_api
async def create_order(item_id, store_id, currency_id, count, payment_backend):
    kwargs = {
        'item_id': item_id,
        'currency_id': currency_id,
        'count': count,
        'payment_backend': payment_backend,
        'user_id': None,
        'payment_kwargs': None,
        'store_id': store_id
    }
    order_data = await store_request('create_order', **kwargs)
    return order_data


@session_api
async def update_order(order_id):
    raise NotImplementedError
