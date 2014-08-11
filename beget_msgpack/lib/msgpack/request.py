# -*- coding: utf-8 -*-

import msgpackrpc
import beget_msgpack
from ..logger import Logger
import traceback


class Request(object):
    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
        self.logger = Logger.get_logger()

    def request(self, route, **kwargs):
        self.logger.debug('msgpack->Request->request:\n'
                          '  host: %s\n'
                          '  port: %s\n'
                          '  route: %s\n'
                          '  arguments: %s\n', self.host, self.port, route, repr(kwargs))

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
        except Exception as e:
            self.logger.error('msgpack->Request: Exception: %s\n'
                              '  %s', e.message, traceback.format_exc())
            response = response_factory.get_response_by_request_error(description=str(e))

        return response

    def do(self, route, **kwargs):
        """alias"""
        return self.request(route, **kwargs)
