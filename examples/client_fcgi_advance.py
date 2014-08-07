#!/usr/bin/env python
# -*- coding: utf-8 -*-

import beget_msgpack
import config


server = 'kon'

request_factory = beget_msgpack.RequestFactory(config)
Request = request_factory.get_request(server)

# Простой пример:
Response = Request.request('index/index', order_id='order_id_string', dump_info_params=['msg1', 'msg2'])

if Response.has_error():
    print repr(Response.get_error())
else:
    print repr(Response.get_method_result())


# Проверка возвращаемых данных:

def print_result_when_send(arg):
    Response = Request.request('index/test', my_arg=arg)
    if Response.has_error():
        print 'Error: %s' % repr(Response.get_error())
    else:
        print repr(Response.get_method_result())
        print 'Type: %s' % type(Response.get_method_result())
        print 'Same: %s' % (arg == Response.get_method_result())

print_result_when_send(1)
print_result_when_send('some')
print_result_when_send('абвгд')  # из php+msgpack возвращает строки в unicode
print_result_when_send(u'абвгд')