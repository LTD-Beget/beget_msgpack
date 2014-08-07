# -*- coding: utf-8 -*-

TYPE_FCGI = 'fcgi'
TYPE_MSGPACK = 'msgpack'

# todo: сделать доступ как через ['это'], так и черезе точку.
servers = dict(

    # используется по умолнчаению
    # todo: сделать слияние конфигов. Сначала берем default, а поверх накладываем конфиг сервера если такой есть
    default=dict(
        type=TYPE_MSGPACK
    ),

    kon=dict(
        type=TYPE_FCGI,
        host='kon.ru',
        port='12345',
        script_dir='/home/path/to/project',
        script_name='index.php',
        secret='mysecret'
    ),

    sul=dict(
        type=TYPE_MSGPACK,
        host='sul.ru',
        port='4444',
    ),

    custom_name_server=dict(
        type=TYPE_MSGPACK,
        host='192.168.2.1'
    ),

    localhost=dict(
        type=TYPE_MSGPACK,
        host='localhost',
        port='50001'
    )
)

msgpack_server = dict(
    default=dict(
        port='50001',
        host='localhost',
        controller_prefix='controllers_msgpack'
    )
)