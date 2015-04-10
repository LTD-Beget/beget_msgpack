# -*- coding: utf-8 -*-

import traceback
from .lib.errors.error_constructor import ErrorConstructor


class Controller():
    """
    Его следует наследовать в ваших контроллерах.
    Он предоставляет:
      - предоставление self.logger
      - вызов экшена
      - обработку стандартных ошибок
    """

    def __init__(self, action_name, method_args, logger, response):
        self.action_name = action_name
        self.logger = logger

        self._response = response
        self._method_args = method_args

    def start(self):
        return self.run()

    def run(self):
        # Получаем имя экшена
        action_name = "action_%s" % self.action_name
        self.logger.debug('Controller: \n'
                          '  action name: %s\n'
                          '  arguments to action: %s', action_name, repr(self._method_args))

        # Если такого экшена нет, то сообщаем об этом
        try:
            action_method = getattr(self, action_name)
        except AttributeError:
            error_message = "missing action %s" % action_name
            self.logger.error("Controller Exception: %s\n  %s", error_message, traceback.format_exc())
            self._response.add_request_error(ErrorConstructor.TYPE_ERROR_BAD_REQUEST, error_message)
            return self._response.dump()

        # Вызываем метод передавая необходимые параметры
        try:
            self.logger.info('Exec: %s.%s(%s)', self.__class__.__name__, action_name, repr(self._method_args))
            result = action_method(**self._method_args) if self._method_args else action_method()
            self._response.method_result = result

        # Перехватываем ошибки с передаваемыми аргументами
        except TypeError as e:
            self.logger.error("Controller Exception: %s\n  %s", e.message, traceback.format_exc())
            self._response.add_method_error(ErrorConstructor.TYPE_ERROR_ARGUMENT, e.message)

        # Перехватываем любые исключения выкинутые в экшене.
        except Exception as e:
            self.logger.error("Controller Exception: %s\n  %s", e.message, traceback.format_exc())
            self._response.add_method_error(ErrorConstructor.TYPE_ERROR_IN_ACTION, e.message)

        # Записываем результат выполнения
        return self._response.dump()
