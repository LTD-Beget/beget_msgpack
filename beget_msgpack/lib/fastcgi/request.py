# -*- coding: utf-8 -*-

import urllib
import base64
import platform

import beget_msgpack
import umsgpack

from .flup_fcgi_client import FCGIApp
from ..helpers import recursive_str_to_unicode


class Request(object):
    def __init__(self, host, port, root, script, secret):
        self.host = host
        self.port = int(port)
        self.root = root
        self.script = script
        self.secret = secret

    def request(self, method, **kwargs):
        params = recursive_str_to_unicode(kwargs)
        method = method.strip().split('/')

        if len(method) != 2:
            raise Exception('method - must be in \'controller/action\' format')

        q_params = {
            "r": "%s/%s" % (method[0], method[1])
        }

        post_params = {'secret': self.secret,
                       'inputData': base64.b64encode(umsgpack.packb(params))}
        content = urllib.urlencode(post_params)
        params = self._get_cgi_params(q_params, len(content))
        fcgi_request = FCGIApp(host=self.host, port=self.port)
        answer = fcgi_request(params, content)
        response_factory = beget_msgpack.ResponseFactory()
        response = response_factory.get_response_by_fcgi_answer(answer)
        return response

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
