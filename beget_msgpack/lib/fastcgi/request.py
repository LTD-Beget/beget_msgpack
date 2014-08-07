# -*- coding: utf-8 -*-

import urllib
import base64
import platform

# from flup.client import fcgi_app
import umsgpack

import beget_msgpack


class Request(object):

    def __init__(self, host, port, root, script, secret):

        raise NotImplementedError('fastcgi not ready')

        self.host = host
        self.port = int(port)
        self.root = root
        self.script = script
        self.secret = secret

    def request(self, method, **kwargs):
        # params = recursive_str_to_unicode(kwargs)  # todo: проверить с и без перевода в unicode
        params = kwargs
        method = method.strip().split('/')

        if len(method) != 2:
            raise Exception('method - must be in \'controller/action\' format')

        q_params = {
            "r": "%s/%s" % (method[0], method[1])
        }

        post_params = {'secret': self.secret,
                       'inputData': base64.b64encode(umsgpack.packb(params))}

        content = urllib.urlencode(post_params)
        params = self._get_cgi_params(content, q_params, len(content))

        fcgi_request = fcgi_app.FCGIApp(host=self.host, port=self.port)
        answer = fcgi_request(params, dummy_def)
        response_factory = beget_msgpack.ResponseFactory()
        response = response_factory.get_response_by_fcgi_answer(answer)
        return response

    def _get_cgi_params(self, content, q_params, content_length):
        return {
            'wsgi.input': content,
            'GATEWAY_INTERFACE': 'FastCGI/1.0',
            'REQUEST_METHOD': 'POST',
            'SCRIPT_FILENAME': self.get_path_script(),
            'SCRIPT_NAME': self.get_path_script(),
            'QUERY_STRING': urllib.urlencode(q_params),
            'REQUEST_URI': self.get_document_uri(),
            'DOCUMENT_URI': self.get_document_uri(),
            'SERVER_SOFTWARE': 'php/fcgiclient',
            'REMOTE_ADDR': '1.2.3.4',  # todo: должен передаваться с конфигом - интерфесов может быть много
                                               # todo: + подключение к стороннему сервису слишком долгая операция
            'REMOTE_PORT': '9985',
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


def dummy_def(*args, **kwargs):
    for count, thing in enumerate(args):
        print '===== args ====='
        print '{0}. {1}'.format(count, thing)

    for name, value in kwargs.items():
        print '===== kwargs ====='
        print '{0} = {1}'.format(name, value)