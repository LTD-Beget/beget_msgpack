#!/usr/bin/env python
# -*- coding: utf-8 -*-

import beget_msgpack
import config

from controllers_msgpack import *

# msgpack сервер
local_config = config.msgpack_server['default']

Service = beget_msgpack.Server(local_config['host'],
                               local_config['port'],
                               local_config['controller_prefix'])
Service.start()
