from v8py import Context, Script, JSException, new
from exec.api.session import session_api
from exec.utils import stdlib
from exec.utils.session import JSSession, JSSessionError
import logging
import os


logger = logging.getLogger('anthill.application')


class JSBuildError(Exception):
    pass


class ClassDoesNotExist(Exception):
    pass


class JSBuild:
    def __init__(self, source_path=None):
        self.context = Context()
        self.promise_type = self.context.glob.Promise
        self.cache = None

        try:
            script = Script(source=stdlib.source, filename=stdlib.name)
            self.context.eval(script)
        except Exception as e:
            raise JSBuildError('Error while compiling stdlib.js') from e

        if source_path:
            for file_name in os.listdir(source_path):
                if not file_name.endswith('.js'):
                    continue

                logger.info('Compiling file {0}.'.format(os.path.join(source_path, file_name)))

                try:
                    with open(os.path.join(source_path, file_name), encoding='utf8') as f:
                        script = Script(source=f.read(), filename=file_name)
                        self.context.eval(script)
                except Exception as e:
                    raise JSBuildError('Error while compiling') from e

        session_api.expose(self.context)

    def add_source(self, source_code, filename=None):
        script = Script(source=source_code, filename=filename)
        try:
            self.context.eval(script)
        except JSException as e:
            raise JSBuildError('Error while adding source') from e

    def create_session(self, handler, class_name, args, **env):
        if class_name not in self.context.glob:
            raise ClassDoesNotExist

        clazz = getattr(self.context.glob, class_name)

        if not getattr(clazz, 'allow_session', False):
            raise ClassDoesNotExist

        try:
            instance = new(clazz, args, env)
        except (TypeError, JSException) as e:
            raise JSSessionError('Failed to build session') from e

        js_session = JSSession(handler, self, instance, self.promise_type, **env)
        return js_session
