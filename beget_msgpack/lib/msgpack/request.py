# -*- coding: utf-8 -*-

import msgpackrpc
from msgpackrpc.error import TimeoutError, TransportError
import beget_msgpack
import traceback
import socket
from ..logger import Logger
from ..errors.error_constructor import ErrorConstructor


class Request(object):

    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
        self.logger = Logger.get_logger()

    def request(self, route, **kwargs):
        """
        Метод выполняющий обращение msgpackrpc и возвращающий ответ
        """

        self.logger.debug('msgpack->Request->request:\n'
                          '  host: %s\n'
                          '  port: %s\n'
                          '  route: %s\n'
                          '  arguments: %s\n', self.host, self.port, route, repr(kwargs))

        # Провереяем переданный controller/action
        if len(route.split("/")) != 2:
            error_msg = "Route must be in 'controller/action' format"
            self.logger.error(error_msg)
            raise StandardError(error_msg)

        response_factory = beget_msgpack.ResponseFactory()

        try:
            client = msgpackrpc.Client(msgpackrpc.Address(self.host, self.port))
            self.logger.info('request to: %s,  route: %s,  args:%s', self.host, route, repr(kwargs))
            answer = client.call(route, kwargs)
            self.logger.debug('msgpack->Request: get answer: %s', answer)
            response = response_factory.get_response_by_msgpack_answer(answer)
            self.logger.info('result of request: %s', response.get_method_result())

        # Перехватываем ошибки подключения и возвращаем информацию о проблеме.
        except (msgpackrpc.error.TimeoutError, msgpackrpc.error.TransportError, socket.gaierror) as e:
            self.logger.error('msgpack->Request: Exception: Can\'t connect: %s\n'
                              '  %s', e.message, traceback.format_exc())
            response = response_factory.get_response_by_request_error(ErrorConstructor.TYPE_ERROR_CONNECTION,
                                                                      str(e),
                                                                      ErrorConstructor.CODE_ERROR_CONNECTION)
        # Перехватываем все остальные ошибки
        except Exception as e:
            self.logger.error('msgpack->Request: Exception: %s\n'
                              '  %s', e.message, traceback.format_exc())
            response = response_factory.get_response_by_request_error(message=str(e))

        return response

    def do(self, route, **kwargs):
        """alias"""
        return self.request(route, **kwargs)
