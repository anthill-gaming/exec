from anthill.platform.api.internal import connector
from anthill.framework.utils.ip import get_ip
from functools import partial
from . import session_api


store_request = partial(connector.internal_request, 'store')


@session_api
async def create_order(item_id, store_id, currency_id, count, payment_backend, session=None):
    user = session.handler.current_user
    payment_kwargs = {
        'ip': get_ip(session.handler.request)
    }
    kwargs = {
        'item_id': item_id,
        'currency_id': currency_id,
        'count': count,
        'payment_backend': payment_backend,
        'user_id': user.id,
        'payment_kwargs': payment_kwargs,
        'store_id': store_id
    }
    order_data = await store_request('create_order', **kwargs)
    return order_data


@session_api
async def update_order(order_id, session=None):
    raise NotImplementedError
