# -*- coding: utf-8 -*-

import sys
import re
import traceback
from msgpackrpc.server import AsyncResult
from .lib.response import Response
from .lib.logger import Logger


class Handler(object):
    def __init__(self, controllers_prefix):
        self.logger = Logger.get_logger()
        self.route = None
        self.controllers_prefix = controllers_prefix

    def __getattr__(self, route):
        self.logger.debug('Handler: __getattr__(%s)', repr(route))
        self.route = route
        try:
            front_controller = FrontController(route, self.controllers_prefix, self.logger)
            return front_controller.run_controller
        except Exception as e:
            self.logger.error('Handler: get Exception: %s\n'
                              'Traceback: %s', e.message, traceback.format_exc())
            raise e


class FrontController(object):
    def __init__(self, route, controllers_prefix, logger):
        self.route = route
        self.controllers_prefix = controllers_prefix
        self.logger = logger

    def run_controller(self, args):
        self.logger.debug('FrontController: get args: %s', repr(args))
        response = Response()
        result = AsyncResult()

        try:
            controller_cls, action = self._parse_route()
            method_args = self._parse_params(args)

            controller = controller_cls(action, method_args, result, self.logger, response)
            controller.start()
        except (ParseParamsError, ParseRouteError) as e:
            response.add_request_error(Response.REQUEST_ERROR_BAD_REQUEST, e.message)
            result.set_result(response.dump())
        except Exception as e:
            self.logger.error('FrontController: Exception: %s\n'
                              '  Traceback: %s', e.message, traceback.format_exc())
            response.add_request_error(Response.REQUEST_ERROR_TYPE_UNKNOWN, e.message)
            result.set_result(response.dump())

        return result

    def _parse_route(self):
        try:
            (cls, action) = self.route.split("/")
            controller_module = self._from_camelcase_to_underscore(cls) + "_controller"
            controller_cls = cls[0].title() + cls[1:] + "Controller"
            module_name = '%s.%s' % (self.controllers_prefix, controller_module)
            self.logger.debug('FrontController: \n'
                              '  module controller: %s\n'
                              '  class controller: %s\n'
                              '  action in controller: %s', module_name, controller_cls, action)
            module_obj = sys.modules[module_name]

            return getattr(module_obj, controller_cls), action
        except Exception as e:
            error_msg = "Failed to parse route or get controller. given: %s" % self.route
            self.logger.error('FrontController: %s\n'
                              '  Exception: %s\n'
                              '  Traceback: %s', error_msg, e.message, traceback.format_exc())
            raise ParseRouteError(error_msg)

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