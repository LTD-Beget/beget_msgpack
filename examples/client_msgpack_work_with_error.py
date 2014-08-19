#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import pydevd
# pydevd.settrace('213.33.252.58', port=9014, stdoutToServer=True, stderrToServer=True)

import beget_msgpack
import examples.config as config

import logging
logging.basicConfig(level=logging.INFO)
logger = beget_msgpack.Logger.get_logger()
logger.setLevel(logging.DEBUG)


def work_with_response(response_target):
    # Получаем любые ошибки
    if response_target.has_error():
        print 'i`m has error:', response_target.get_error()

    # Получаем ошибки запроса
    if response_target.has_request_error():
        print 'has request error:', response_target.get_request_error()

    # Получаем ошибки метода
    if response_target.has_method_errors():
        print 'has method error:', response_target.get_method_error()

    # Получаем итератор по ошибкам.
    errors_iterator = response_target.get_error()  # or get_request_error(), or get_method_error()
    if errors_iterator:
        print 'ErrorIterator to string (first error message):', str(errors_iterator)
        print 'Start ErrorIterator'
        for error in errors_iterator:
            print 'Error: %s' % repr(error)
            print 'Error message: %s' % error.message
        print 'End ErrorIterator'

    # Если ошибок небыло, то отображаем результат запроса
    if not response.has_error():
        print 'Method result: ', repr(response.get_method_result())


# server = 'kon'  # Для этого сервера должен вернуться запрос для fastcgi
# server = 'sul'  # Для этого сервера должен вернуться запрос для msgpack.client
# server = 'localhost'
server = 'localhost'

# Обращаемся к фабрике запросов указывая сервер к которому мы будем отправлять запрос.
# Из фабрики получаем класс запроса
request_factory = beget_msgpack.RequestFactory(config)
Request = request_factory.get_request(server)

print '\n\n----------\nRequest without error:\n'
response = Request.request('test/test', my_arg='my argument')
work_with_response(response)  # Get request error: ErrorArgument


print '\n\n----------\nError with missing action:\n'
response = Request.request('test/uncreated')
work_with_response(response)  # Get request error: ErrorArgument
                              # with message: missing action action_uncreated

print '\n\n----------\nError with missing controller:\n'
response = Request.request('uncreated/test')
work_with_response(response)  # Get request error: ErrorBadRequest
                              # with message: Failed to parse route or get controller. given: uncreated/test

print '\n\n----------\nError with missing arguments:\n'
response = Request.request('test/test')
work_with_response(response)  # Get method error: ErrorArgument
                              # with message: action_test() takes exactly 2 arguments (1 given)

print '\n\n----------\nError with wrong name argument:\n'
response = Request.request('test/test', bad_name_argument='some')
work_with_response(response)  # Get method error: ErrorArgument
                              # with message: action_test() got an unexpected keyword argument 'bad_name_argument'

print '\n\n----------\nError with exception in action (user code):\n'
response = Request.request('test/error')
work_with_response(response)  # Get method error: ErrorAction
                              # with message: This is standard Exception

print '\n\n----------\nError with bad hostname:\n'
Request = request_factory.get_request('uncreated-hostname.org')
response = Request.request('test/test')
work_with_response(response)  # Get request error: ErrorConnection
                              # with message: [Errno -2] Name or service not known

print '\n\n----------\nError with bad port:\n'
Request = request_factory.get_request('192.168.2.2')  # random server where not started MsgPackServer
response = Request.request('test/test')
work_with_response(response)  # Get request error: ErrorConnection
                              # with message: Retry connection over the limit


Request = request_factory.get_request('kondr')


print '\n\n----------\nError fcgi with missing controller:\n'
response = Request.request('sdindex/index', order_id='myOrder_id', dump_info_params=['one', 'two'])
work_with_response(response)  # Get request error: ErrorBadRequest
                              # with message: Unable to resolve the request "sdindex/index".

print '\n\n----------\nError fcgi with missing action:\n'
response = Request.request('index/indexe', order_id='myOrder_id', dump_info_params=['one', 'two'])
work_with_response(response)  # Get request error: ErrorBadRequest
                              # with message: Unable to resolve the request: index/indexe

print '\n\n----------\nError fcgi with missing arguments:\n'
response = Request.request('index/index')
work_with_response(response)  # Get request error: ErrorBadRequest
                              # with message: Unable to resolve the request: index/indexe

print '\n\n----------\nError fcgi with wrong arguments:\n'
response = Request.request('index/index', bad_name_argument='myOrder_id', dump_info_params=['one', 'two'])
work_with_response(response)  # Get request error: ErrorBadRequest
                              # with message: Unable to resolve the request: index/indexe

print '\n\n----------\nError fcgi with wrong arguments:\n'
response = Request.request('index/index', bad_name_argument='myOrder_id', dump_info_params=['one', 'two'])
work_with_response(response)  # Get request error: ErrorBadRequest
                              # with message: Unable to resolve the request: index/indexe

print '\n\n----------\nError with exception in action (user code):\n'
response = Request.request('index/error')
work_with_response(response)  # Get method error: ErrorAction
                              # with message: Custom message in Exception

print '\n\n----------\nError with bad hostname:\n'
Request = request_factory.get_request('kon')
response = Request.request('test/test')
work_with_response(response)  # Get request error: ErrorConnection
                              # with message: [Errno -2] Name or service not known

print '\n\n----------\nError with bad port:\n'
Request = request_factory.get_request('kon')  # random server where not started FCGIMsgPackServer
response = Request.request('test/test')
work_with_response(response)  # Get request error: ErrorConnection
                              # with message: [Errno 111] Connection refused


print '\n\nNormal exit'