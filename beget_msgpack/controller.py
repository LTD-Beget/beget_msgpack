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
            self.logger.error("Controller Exception: %s\n"
                              "  %s", e.message, traceback.format_exc())
            self._response.add_method_error(self._response.METHOD_ERROR_TYPE_ARGUMENT, e.message)

        except Exception as e:
            self.logger.error("Controller Exception: %s\n"
                              "  %s", e.message, traceback.format_exc())
            self._response.add_method_error(self._response.METHOD_ERROR_TYPE_UNKNOWN, e.message)

        finally:
            self._result.set_result(self._response.dump())

    def _run_action(self):
        action_name = "action_%s" % self.action_name
        self.logger.debug('Controller: \n'
                          '  action name: %s\n'
                          '  arguments to action: %s', action_name, repr(self._method_args))

        try:
            action_method = getattr(self, action_name)
        except:
            raise Exception("missing action %s" % action_name)

        self.logger.info('Exec: %s.%s(%s)', self.__class__.__name__, action_name, repr(self._method_args))
        result = action_method(**self._method_args) if self._method_args else action_method()
        self._response.method_result = result
