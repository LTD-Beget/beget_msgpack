#!/usr/bin/env python
# -*- coding: utf-8 -*-

import beget_msgpack
from config import HOST, PORT

Request = beget_msgpack.Request(HOST, PORT)


# argument types examples:

Response = Request.request('test/test', my_arg='custom_arg')
print repr(Response.get_method_result())

Response = Request.request('test/test', my_arg=43)
print repr(Response.get_method_result())

Response = Request.request('test/test', my_arg=['one', 'two'])
print repr(Response.get_method_result())

Response = Request.request('test/test', my_arg={'key': 'val'})
print repr(Response.get_method_result())


# error handling examples:

Response = Request.request('test/error')
if Response.has_error():
    print 'i`m has error: %s' % Response.get_error()
else:
    print 'i don`t have error'


# utf8 examples:

msg = 'Шла Саша по шоссе'
Response = Request.request('test/test', my_arg=msg)
answer = Response.get_method_result()
print 'UTF8 answer by str: %s' % answer['return']
print 'UTF8 by str compare: %s' % (msg == answer['return'])

msg = u'Шла Саша по шоссе'
Response = Request.request('test/test', my_arg=msg)
answer = Response.get_method_result()
print 'UTF8 answer by unicode: %s' % answer['return']
print 'UTF8 by bytes compare: %s' % (msg == answer['return'].decode('utf-8'))