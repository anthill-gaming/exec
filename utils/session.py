from v8py import JSException, JSPromise, Context, new, JavaScriptTerminated
from tornado.gen import with_timeout, TimeoutError, Future
from exec.api.v1.session import SessionAPIError
from datetime import timedelta
import logging


logger = logging.getLogger('anthill.application')


class JSExecutionError(Exception):
    def __init__(self, code=None, message=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code or 500
        self.message = message or 'Javascript execution error'

    def __str__(self):
        return self.message


class JSSessionError(Exception):
    pass


class JSSessionCallTimeoutError(Exception):
    pass


class JSSession:
    call_timeout = 10

    def __init__(self, handler, build, instance, promise_type, **env):
        self.handler = handler
        self.build = build
        self.instance = instance
        self.promise_type = promise_type
        self.env = env

    async def configure(self):
        """Additional configuration for javascript session."""
        raise NotImplementedError

    async def open(self):
        """Open javascript session."""
        raise NotImplementedError

    async def close(self, code, reason):
        """Close javascript session."""
        raise NotImplementedError

    async def call(self, method_name, args):
        """Call javascript session api method."""
        context = self.build.context

        method = getattr(self.instance, method_name)

        try:
            future = context.async_call(method, (args,), JSFuture)
        except JSException as e:
            raise JSExecutionError from e
        except SessionAPIError as e:
            # raise JSExecutionError(message=str(e)) from e
            raise
        except Exception as e:
            raise JSExecutionError from e

        if future.done():
            return future.result()

        try:
            result = await with_timeout(timedelta(seconds=self.call_timeout), future)
            return result
        except TimeoutError as e:
            raise JSSessionCallTimeoutError from e
        finally:
            future._result = None
