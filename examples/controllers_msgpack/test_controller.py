# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import beget_msgpack
import time

class TestController(beget_msgpack.Controller):

    def action_test(self, my_arg):
        print 'start sleep'
        time.sleep(35)
        print 'end sleep'
        print 'Controller get: %s' % repr(my_arg)
        return {'return': my_arg}

    def action_error(self):
        raise Exception('This is standard Exception')

    def action_get_custom_exception(self):
        raise NotImplementedError('NotImplementedError exception')
