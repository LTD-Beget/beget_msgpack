# -*- coding: utf-8 -*-

import msgpackrpc
import signal
import traceback
import handler
import socket
import sys
from lib.logger import Logger


class Server():
    """
    Msgpack сервере. Работает с контроллерами, обертка над msgpackrpc
    """

    def __init__(self, host, port, controllers_prefix, logger_name=None):
        print '==================   my msgpack'
        self.logger = Logger.get_logger(logger_name)
        self.controllers_prefix = controllers_prefix
        self.handler = handler.Handler(controllers_prefix)
        self.host = str(host)
        self.port = int(port)

    def start(self):
        try:
            server = msgpackrpc.Server(self.handler)

            def stop(num, stackframe):
                self.logger.critical("Server: get signal %s and stop", num)

                try:
                    server.close()
                    self.logger.critical("Server: after close")
                    server.stop()
                    self.logger.critical("Server: after stop")
                except Exception as e:
                    self.logger.error("Error on msgpackrpc server stop: %s\n %s", e.message, traceback.format_exc())

                sys.exit()

            signal.signal(signal.SIGTERM, stop)
            signal.signal(signal.SIGINT, stop)

            self.logger.info('Server: listen: %s:%s', self.host, self.port)
            server.listen(msgpackrpc.Address(self.host, self.port, socket.AF_INET))
            server.start()
        except Exception as e:
            self.logger.error('Server: get exception: %s\n'
                              'traceback: %s', e.message, traceback.format_exc())
