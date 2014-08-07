#!/usr/bin/env python
# -*- coding: utf-8 -*-

import beget_msgpack
import config


# server = 'kon'  # Для этого сервера должен вернуться запрос для fastcgi
server = 'sul'  # Для этого сервера должен вернуться запрос для msgpack.client
# server = 'localhost'

# Обращаемся к фабрике запросов указывая сервер к которому мы будем отправлять запрос.
# Из фабрики получаем класс реквеста

request_factory = beget_msgpack.RequestFactory(config)
Request = request_factory.get_request(server)

# (Действия дальше идентичны для любого реквеста возврващаемого из фабрики)
# Делаем реквест с указанием контроллера/экшена и аргументов
# Response = Request.request('myControllerName/myActionName', my_arg='myMsg')
Response = Request.request('test/test', domain_id='myMsg')

# Из реквеста получаем Response
print Response.get_method_result()
