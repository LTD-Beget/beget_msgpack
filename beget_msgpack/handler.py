# -*- coding: utf-8 -*-

import select
import sys
import re
import traceback
import msgpack

import preforkserver as pfs

from .lib.logger import Logger
from .lib.response import Response
from .lib.errors.error_constructor import ErrorConstructor


class Handler(pfs.BaseChild):
    """
    Класс который обслуживает коннект. Является форком по средством prefork библиотеки
    """

    def initialize(self, controllers_prefix, timeout_receive=5):
        """
        Кастомный __init__ от библиотеки prefork
        """
        self.controllers_prefix = controllers_prefix
        self.logger = Logger.get_logger()
        self.packer = msgpack.Packer(default=lambda x: x.to_msgpack())
        self.unpacker = msgpack.Unpacker()
        self.response = Response()
        self.timeout_receive = timeout_receive

    def process_request(self):
        """
        Обработчик запроса (когда происходит передача данных на сервер)
        """
        try:

            # Получаем все данные из сокета
            message = ''
            data = ''
            while True:

                # Устанавливаем таймаут на получение данных из сокета
                ready = select.select([self.conn], [], [], self.timeout_receive)
                if ready[0]:
                    data_buffer = self.conn.recv(4096)
                else:
                    raise Exception('Exceeded timeout')

                # msgpack-rpc не завершает данные EOF, поэтому через not data мы не выйдем
                if not data_buffer:
                    raise Exception('Only for MessagePack')

                data += data_buffer

                try:
                    # Выходим если получилось декодировать, иначе продолжаем ожидать данные
                    message = msgpack.unpackb(data)
                    break
                except:
                    pass

            self.on_message(message)

        except Exception as e:
            #Выброс ошибки выше, влечен проблемы с воркерами
            self.logger.error('Handler: get Exception: %s\n  Traceback: %s', e.message, traceback.format_exc())

    def on_message(self, message):
        route = message[2]
        arguments = message[3][0]
        self.logger.debug('Handler: \n  Route: %s\n  Arguments: %s', repr(route), repr(arguments))

        front_controller = FrontController(route, self.controllers_prefix, self.logger)
        result = front_controller.run_controller(arguments)

        result_encoded = self.packer.pack([1, 0, None, result])
        self.conn.sendall(result_encoded)


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
        response = Response()

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
            return response.dump()

        # Вызываем контроллер и передаем ему необходимыем параметры
        try:
            controller = controller_class(action, action_args, self.logger, response)
            result = controller.start()
            return result

        except Exception as e:
            self.logger.error('FrontController: Exception: %s\n  Traceback: %s', e.message, traceback.format_exc())
            response.add_request_error(ErrorConstructor.TYPE_ERROR_UNKNOWN, e.message)
        return response.dump()

    @staticmethod
    def _from_camelcase_to_underscore(string):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
