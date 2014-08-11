#!/usr/bin/env python
# -*- coding: utf-8 -*-

import beget_msgpack
import examples.config as config
import logging

from controllers_msgpack import *


print 'test'

logging.basicConfig(level=logging.CRITICAL)

logger = logging.getLogger('beget_msgpack_custom')
# logger = beget_msgpack.Logger.get_logger()  # Get logger of package. And same time you can set name of logger.
logger.setLevel(logging.DEBUG)

local_config = config.msgpack_server['default']
Service = beget_msgpack.Server(local_config['host'],
                               local_config['port'],
                               local_config['controller_prefix'],
                               'beget_msgpack_custom')
Service.start()
