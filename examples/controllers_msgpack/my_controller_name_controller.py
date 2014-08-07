# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import beget_msgpack


class MyControllerNameController(beget_msgpack.Controller):

    def action_myActionName(self, my_arg):
        print 'Controller get: %s' % repr(my_arg)
        return {'return': my_arg}