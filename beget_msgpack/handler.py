# -*- coding: utf-8 -*-

import sys
import re
import traceback
from msgpackrpc.server import AsyncResult
from response import Response
import logging


class Handler(object):
    def __init__(self, controllers_prefix, logger=None):
        self.route = None
        self.controllers_prefix = controllers_prefix

        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger()
            self.logger.disabled = True

    def __getattr__(self, item):
        self.logger.debug('item: ' + repr(item))
        self.route = item
        try:
            front_controller = FrontController(item, self.controllers_prefix, self.logger)
            return front_controller.run_controller
        except Exception as e:
            print e
            raise e


class FrontController(object):
    def __init__(self, route, controllers_prefix, logger):
        self.route = route
        self.controllers_prefix = controllers_prefix
        self.logger = logger

    def run_controller(self, args):
        self.logger.debug('args: %s' % args)
        response = Response()
        result = AsyncResult()

        try:
            controller_cls, action = self._parse_route()
            method_args = self._parse_params(args)

            controller = controller_cls(action, method_args, result, self.logger, response)
            controller.start()
        except (ParseParamsError, ParseRouteError) as e:
            self.logger.error(e.message)
            response.add_request_error(Response.REQUEST_ERROR_BAD_REQUEST, e.message)
            result.set_result(response.dump())
        except Exception as e:
            self.logger.error("%s\n%s", traceback.format_exc(), e.message)
            response.add_request_error(Response.REQUEST_ERROR_TYPE_INTERNAL, e.message)
            result.set_result(response.dump())

        return result

    def _parse_route(self):
        try:
            (cls, action) = self.route.split("/")
            controller_module = self._from_camelcase_to_underscore(cls) + "_controller"
            controller_cls = cls[0].title() + cls[1:] + "Controller"
            a = sys.modules['%s.%s' % (self.controllers_prefix, controller_module)]

            return getattr(a, controller_cls), action
        except Exception as e:
            raise ParseRouteError("Failed to parse route or get controller. given: %s" % self.route)

    def _parse_params(self, params):
        return params

    @staticmethod
    def _from_camelcase_to_underscore(string):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class ParseRouteError(Exception):
    pass


class ParseParamsError(Exception):
    pass