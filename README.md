Basic usage
============

    git clone https://github.com/LTD-Beget/beget_msgpack

    apt-get install python-pip  #pip required

    cd beget_msgpack/
    python setup.py install

    cd examples/
    python test_controller.py   # Get test message
    python send_message.py      # Send test message (use this when test_controller working)


Alternative usage
============
Installation:

    pip install beget_msgpack

Request script:
```python
import beget_msgpack
from config import host, port

Request = beget_msgpack.Request(host, port)

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