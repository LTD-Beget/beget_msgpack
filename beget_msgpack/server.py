# -*- coding: utf-8 -*-

import traceback

from .handler import Handler
from .lib.logger import Logger

import SocketServer

import signal
import socket
import os


class VendorServer(SocketServer.ForkingTCPServer, object):

    def __init__(self, server_address, request_handler_class, bind_and_activate=True,
                 child_kwargs=None, max_servers=5, timeout_receive=30, request_queue_size=30):

        self.child_kwargs = child_kwargs if child_kwargs is not None else {}
        self.timeout_receive = timeout_receive
        self.request_queue_size = request_queue_size
        self.max_children = max_servers

        super(VendorServer, self).__init__(server_address, request_handler_class, bind_and_activate)

    def server_bind(self):
        try:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except:
            pass
        self.allow_reuse_address = True
        super(VendorServer, self).server_bind()

    def process_request(self, request, client_address):
        """Fork a new subprocess to process the request."""
        self.collect_children()
        pid = os.fork()
        if pid:
            # Parent process
            if self.active_children is None:
                self.active_children = set()
            self.active_children.add(pid)
            self.close_request(request)  #close handle in parent process
            return
        else:
            # Child process.
            # This must never return, hence os._exit()!
            try:
                self.socket.close()  # children don't need server-listening socket
                signal.signal(signal.SIGCHLD, signal.SIG_DFL)
                self.RequestHandlerClass(request, client_address, self, **self.child_kwargs)
                self.shutdown_request(request)
                os._exit(0)
            except:
                try:
                    self.handle_error(request, client_address)
                    self.shutdown_request(request)
                finally:
                    os._exit(1)

    def run(self):
        self.set_signals()
        self.serve_forever()

    def set_signals(self):
        signal.signal(signal.SIGCHLD, self.handle_sigchld)

    def handle_sigchld(self, signum, frame):
        os.waitpid(-1, os.WNOHANG)


class Server():

    def __init__(self, host, port, controllers_prefix, max_servers=5, timeout_receive=5, logger_name=None):
        self.logger = Logger.get_logger(logger_name)
        self.controllers_prefix = controllers_prefix
        self.host = str(host)
        self.port = int(port)
        self.max_servers = max_servers
        self.timeout_receive = timeout_receive

    def start(self):
        try:
            self.logger.info('Server: listen: %s:%s', self.host, self.port)

            child_kwargs = {
                'controllers_prefix': self.controllers_prefix,
                'timeout_receive': self.timeout_receive
            }

            manager = VendorServer((self.host, self.port), Handler, child_kwargs=child_kwargs,
                                   max_servers=self.max_servers, timeout_receive=self.timeout_receive)
            manager.run()
        except Exception as e:
            self.logger.error('Server: get exception: %s\n traceback: %s', e.message, traceback.format_exc())
