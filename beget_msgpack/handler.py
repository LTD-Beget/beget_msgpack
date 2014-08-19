# -*- coding: utf-8 -*-

import sys
import re
import traceback
from msgpackrpc.server import AsyncResult
from .lib.response import Response
from .lib.logger import Logger
from .lib.errors.error_constructor import ErrorConstructor


class Handler(object):
    """
    обработчик для msgpackrpc.Server
    Каждый раз когда msgpackrpc.Server получает сообщение, он его передает в то, что вернет __getattr__ этого класса
    """

    def __init__(self, controllers_prefix):
        """
        :param controllers_prefix: имя пакета (префикс) где будут искаться контроллеры
        :type controllers_prefix: str
        """
        self.logger = Logger.get_logger()
        self.controllers_prefix = controllers_prefix

    def __getattr__(self, route):
        """
        :param route: получает путь к экшену в виде 'controller/action'
        :type route: str
        """
        self.logger.debug('Handler: __getattr__(%s)', repr(route))
        try:
            front_controller = FrontController(route, self.controllers_prefix, self.logger)
            return front_controller.run_controller
        except Exception as e:
            self.logger.error('Handler: get Exception: %s\n'
                              'Traceback: %s', e.message, traceback.format_exc())
            raise e


class FrontController(object):
    """
    Класс обработчик запросов
    Он отвечает за:
        - получение и вызов контроллера с передачей ему параметров (имя экшена, аргументы)
        - обработка ошибок
    """

    def __init__(self, route, controllers_prefix, logger):
        """
        :param route: получает путь к экшену в виде 'controller/action'
        :type route: str

        :param controllers_prefix: имя пакета (префикс) где будут искаться контроллеры
        :type controllers_prefix: str
        """
        self.route = route
        self.controllers_prefix = controllers_prefix
        self.logger = logger

    def run_controller(self, action_args):
        """
        :param action_args: получает dict аргументов или пустой dict
        :type action_args: dict
        """

        self.logger.debug('FrontController: get args: %s', repr(action_args))

        response = Response()
        result = AsyncResult()

        # Ищем вызываемый контроллер
        try:
            (controller_name_search, action) = self.route.split("/")
            controller_name = controller_name_search[0].title() + controller_name_search[1:] + "Controller"
            controller_module_name = self._from_camelcase_to_underscore(controller_name_search) + "_controller"
            module_name = '%s.%s' % (self.controllers_prefix, controller_module_name)
            self.logger.debug('FrontController: \n'
                              '  module controller: %s\n'
                              '  class controller: %s\n'
                              '  action in controller: %s', module_name, controller_name, action)
            module_obj = sys.modules[module_name]
            controller_class = getattr(module_obj, controller_name)

        # Если контроллера нет, то возвращаем ошибку запроса
        except Exception as e:
            error_msg = "Failed to parse route or get controller. given: %s" % self.route
            self.logger.error('FrontController: %s\n  Exception: %s\n'
                              '  Traceback: %s', error_msg, e.message, traceback.format_exc())
            response.add_request_error(ErrorConstructor.TYPE_ERROR_BAD_REQUEST, error_msg)
            result.set_result(response.dump())
            return result

        # Вызываем контроллер и передаем ему необходимыем параметры
        try:
            controller = controller_class(action, action_args, result, self.logger, response)
            controller.start()

        except Exception as e:
            self.logger.error('FrontController: Exception: %s\n  Traceback: %s', e.message, traceback.format_exc())
            response.add_request_error(ErrorConstructor.TYPE_ERROR_UNKNOWN, e.message)
            result.set_result(response.dump())
        return result

    @staticmethod
    def _from_camelcase_to_underscore(string):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
