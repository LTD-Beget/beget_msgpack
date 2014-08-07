# -*- coding: utf-8 -*-

import threading
import traceback


class Controller(threading.Thread):
    def __init__(self, action_name, method_args, result, logger, response):
        threading.Thread.__init__(self)

        self.action_name = action_name
        self.logger = logger

        self._response = response
        self._method_args = method_args
        self._result = result

    def run(self):
        try:
            self._run_action()

        except TypeError as e:
            self.logger.error("%s\n%s", e.message, traceback.format_exc())
            self._response.add_method_error(self._response.METHOD_ERROR_TYPE_ARGUMENT, e.message)

        except Exception as e:
            self.logger.error("%s\n%s", e.message, traceback.format_exc())
            self._response.add_method_error(self._response.METHOD_ERROR_TYPE_UNKNOWN, e.message)

        finally:
            self._result.set_result(self._response.dump())

    def _run_action(self):
        action_name = "action_%s" % self.action_name
        self.logger.debug('action_name: %s' % action_name)

        try:
            action_method = getattr(self, action_name)
        except:
            raise Exception("missing action %s" % action_name)

        self.logger.debug('args: %s' % repr(self._method_args))
        self.logger.debug('action_method: %s' % repr(action_method))
        result = action_method(**self._method_args) if self._method_args else action_method()
        self._response.method_result = result