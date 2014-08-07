

Basic usage
============

    git clone https://github.com/LTD-Beget/beget_msgpack

    apt-get install python-pip  #pip required

    cd beget_msgpack/
    python setup.py install

    cd examples/
    python server.py
    python client.py
    python client_msgpack_advance.py

### Dependent modules

* msgpack-python (>= 0.3)
* tornado (>= 3)
* msgpack-rpc-python
* u-msgpack-python


### Required for install

* pip


Alternative usage
============
Installation:

    pip install beget_msgpack

Request script:
```python
import beget_msgpack
import config  # see examples


request_factory = beget_msgpack.RequestFactory(config)
Request = request_factory.get_request(server)

# 'controller/action' - it tells for default handler which controller and action you want to call
# some_arg= - and all other kwarg -> send to action how arguments
# See the examples for more understanding how to gets arguments.
Response = Request.request('controller/action', some_arg='message_to_kwarg_of_action')
print Response.get_method_result()
```


Server for working with controllers:
```python
import beget_msgpack
from config import host, port

# 'Service' - allows you to start listening msgpack
# controllers_prefix - specifies a prefix for controllers
# See the examples for understanding how to location controllers.
beget_msgpack.Service(host, port, controllers_prefix='controllers_msgpack')
beget_msgpack.start()
```


Tutorial
============

# RequestFactory
Используется для получения запросов независимо от транспорта который должен использоваться.
Фабрика при инициализации получает конфиг в виде dict.
Структура конфига:

  servers = dict(

    # используется по умолнчаению
    default=dict(
        type=TYPE_MSGPACK
        port=60001
    ),

    # имя сервера
    kon=dict(

        # тип подключения [fcgi|msgpack]
        type=TYPE_FCGI,

        # адрес подключения. Если не указан, то используется имя сервера
        host='kon.ru',

        port='12345',

        # fcgi хочет знать о файлу к которому он будет обращаться
        script_dir='/home/path/to/proj',
        script_name='index.php',

        # политика безопасности phportal требует указывать secret при обращение по fcgi
        secret='mySecret'

        # можно указывать любые данные в конфиге. Они будет переданы классу Request где их можно обработать
        custom_variable='some'
    ),

    sul=dict(
        type=TYPE_MSGPACK
    ),

    # кастомное имя сервера
    custom_name_server=dict(
        type=TYPE_MSGPACK,
        host='sul.ru'
    )
  )