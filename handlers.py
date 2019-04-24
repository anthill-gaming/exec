from anthill.platform.handlers.jsonrpc import JsonRPCSessionHandler, jsonrpc_method
from anthill.framework.auth.handlers import UserHandlerMixin
from exec.utils.session import JSSession, JSSessionError


class SessionHandler(UserHandlerMixin, JsonRPCSessionHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(self, application, request, **kwargs)
        self.js_session = None

    def check_origin(self, origin):
        return True

    async def prepare(self):
        await super().prepare()
        self.js_session = build.create_session(self)
        await self.js_session.configure()

    async def open(self, *args, **kwargs):
        await super().open(*args, **kwargs)
        await self.js_session.open()

    async def close(self, code=None, reason=None):
        await self.js_session.close(code, reason)
        await super().close(code, reason)

    @jsonrpc_method()
    async def call(self, method_name, arguments):
        result = await self.js_session.call(method_name, arguments)
        return result
