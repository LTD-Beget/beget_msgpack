# -*- coding: utf-8 -*-

import urllib
import base64
import platform
import re
import traceback
import socket

import beget_msgpack
import msgpack

from .flup_fcgi_client import FCGIApp
from ..logger import Logger
from ..errors.error_constructor import ErrorConstructor


class Request(object):
    def __init__(self, host, port, root, script, secret, timeout=None):
        self.host = host
        self.port = int(port)
        self.root = root
        self.script = script
        self.secret = secret
        self.logger = Logger.get_logger()
        self.timeout = timeout

    def set_timeout(self, sec_int):
        assert isinstance(sec_int, (int, float))
        self.timeout = sec_int

    def request(self, route, **kwargs):
        self.logger.debug('fcgi->Request->request:\n'
                          '  host: %s\n'
                          '  port: %s\n'
                          '  route: %s\n'
                          '  arguments: %s\n', self.host, self.port, route, repr(kwargs))

        route_strip = route.strip().split('/')

        if len(route_strip) != 2:
            error_msg = 'Route: %s  But route - must be in \'controller/action\' format' % route
            self.logger.error(error_msg)
            raise Exception(error_msg)

        controller_name = self.prepare_path_name(route_strip[0])
        action_name = self.prepare_path_name(route_strip[1])
        self.logger.debug('fcgi->Request->request:\n'
                          '  controller: %s\n'
                          '  action: %s', controller_name, action_name)
        q_params = {
            "r": "%s/%s" % (controller_name, action_name)
        }
        post_params = {'secret': self.secret,
                       'inputData': base64.b64encode(msgpack.packb(kwargs))}
        content = urllib.urlencode(post_params)
        params = self._get_cgi_params(q_params, len(content))
        fcgi_request = FCGIApp(host=self.host, port=self.port, timeout=self.timeout)
        response_factory = beget_msgpack.ResponseFactory()
        self.logger.debug('Request: send:\n    params: %s\n    content: %s\n', repr(params), repr(content))
        self.logger.info('request to: %s,  route: %s,  args:%s', self.host, route, repr(kwargs))
        try:
            answer = fcgi_request(params, content)
            response = response_factory.get_response_by_fcgi_answer(answer)
        except (socket.gaierror, socket.error) as e:
            self.logger.error('msgpack->Request: Exception: Can\'t connect: %s\n'
                              '  %s', e.message, traceback.format_exc())
            response = response_factory.get_response_by_request_error(ErrorConstructor.TYPE_ERROR_CONNECTION,
                                                                      str(e),
                                                                      ErrorConstructor.CODE_ERROR_CONNECTION)
        self.logger.info('result of request: %s', response.get_method_result())
        return response

    def do(self, method, **kwargs):
        """alias"""
        return self.request(method, **kwargs)

    def _get_cgi_params(self, q_params, content_length):
        return {
            'GATEWAY_INTERFACE': 'FastCGI/1.0',
            'REQUEST_METHOD': 'POST',
            'SCRIPT_FILENAME': self.get_path_script(),
            'SCRIPT_NAME': self.get_path_script(),
            'QUERY_STRING': urllib.urlencode(q_params),
            'REQUEST_URI': self.get_document_uri(),
            'DOCUMENT_URI': self.get_document_uri(),
            'SERVER_SOFTWARE': 'php/fcgiclient',
            'REMOTE_ADDR': '1.2.3.4',          # todo: должен передаваться с конфигом - интерфесов может быть много
            'REMOTE_PORT': '9985',             # todo: + подключение к стороннему сервису слишком долгая операция
            'SERVER_ADDR': self.host,
            'SERVER_PORT': str(self.port),
            'SERVER_NAME': platform.node(),
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'CONTENT_TYPE': 'application/x-www-form-urlencoded',
            'CONTENT_LENGTH': str(content_length)
        }

    def get_path_script(self):
        return self.root + '/' + self.script

    def get_document_uri(self):
        return '/' + self.script

    def prepare_path_name(self, name):
        name_lowercase_first_char = name[0].lower() + name[1:]
        return self.camel_2_dashed(name_lowercase_first_char)

    def camel_2_dashed(self, string):
        return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '-\\1', string).lower()
