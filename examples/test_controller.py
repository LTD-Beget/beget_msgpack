#!/usr/bin/env python
# -*- coding: utf-8 -*-

import beget_msgpack
from config import HOST, PORT

# Controllers must be imported and are available on the path -> controllers_prefix.controller_name
from controllers_msgpack import *

Service = beget_msgpack.Service(HOST, PORT, controllers_prefix='controllers_msgpack')
Service.start()