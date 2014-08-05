# -*- coding: utf-8 -*-

import msgpackrpc
import signal
import traceback
import handler


class Service():
    def __init__(self, host, port, controllers_prefix):
        self.controllers_prefix = controllers_prefix
        self.handler = handler.Handler(controllers_prefix)
        self.host = str(host)
        self.port = int(port)

    def start(self):
        try:
            server = msgpackrpc.Server(self.handler)

            def stop(num, stackframe):
                print "Got SIGTERM|SIGINT. Bye!"
                server.close()
                server.stop()
                exit(0)

            signal.signal(signal.SIGTERM, stop)
            signal.signal(signal.SIGINT, stop)

            print 'listen: %s:%s' % (self.host, self.port)
            server.listen(msgpackrpc.Address(self.host, self.port))
            server.start()
        except Exception as e:
            print "Got an exception: %s" % e.message
            print traceback.format_exc()