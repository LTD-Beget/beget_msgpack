# -*- coding: utf-8 -*-

import traceback

import preforkserver as pfs

from .handler import Handler
from .lib.logger import Logger


class Server():
    """
    Сервер - обертка для preforkserver. Кодирование - msgpack.
    """

    def __init__(self, host, port, controllers_prefix, max_servers=20, min_servers=5, min_spare_servers=2,
                 max_spare_servers=10, reuse_port=False, timeout_receive=5, logger_name=None):
        self.logger = Logger.get_logger(logger_name)
        self.controllers_prefix = controllers_prefix

        self.host = str(host)
        self.port = int(port)

        self.max_servers = max_servers
        self.min_servers = min_servers
        self.min_spare_servers = min_spare_servers
        self.max_spare_servers = max_spare_servers

        self.reuse_port = reuse_port
        self.timeout_receive = timeout_receive

    def start(self):
        try:
            self.logger.info('Server: listen: %s:%s', self.host, self.port)

            child_kwargs = {
                'controllers_prefix': self.controllers_prefix,
                'timeout_receive': self.timeout_receive
            }

            manager = pfs.Manager(Handler, port=self.port, bind_ip=self.host, child_kwargs=child_kwargs,
                                  max_servers=self.max_servers, min_servers=self.min_servers,
                                  min_spare_servers=self.min_spare_servers, max_spare_servers=self.max_spare_servers,
                                  reuse_port=self.reuse_port)
            manager.run()
        except Exception as e:
            self.logger.error('Server: get exception: %s\n traceback: %s', e.message, traceback.format_exc())
