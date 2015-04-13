# -*- coding: utf-8 -*-

#
# Структура данных при валидном ответе:
#
# status: 'success'
# answer:
#     status: 'success'
#     response: 'сдесь может быть как int, так массив или еще чего'
#
############
#
# Структура данных при ошибке в методе:
# status: 'success'
# answer:
#     status: 'error'
#     errors:
#         TYPE_FIRST: # Тип ошибки. Строка харкодится в коде. В phportal, на ее основе возвращаются разные типы ошибок.
#            [0]:
#                [0]:'error message'
#                [1]:'error code'
#
#            [1]:     # Для одного типа ошибок, может быть несколько самих ошибок
#                [0]:'error message'
#                [1]:'error code'
#         TYPE_SECOND: # может быть несколько типов ошибок
#            [0]:
#                [0]:'error message'
#                [1]:'error code'
#
############
#
# Структура данных при ошибке в запросе:  (Такая же структура как в ошибке метода, но на один уровень выше к корню)
# status: 'error'
# errors:
#     TYPE_FIRST: # Тип ошибки. Строка харкодится в коде. В phportal, на ее основе возвращаются разные типы ошибок.
#        [0]:
#            [0]:'error message'
#            [1]:'error code'
#
#        [1]:     # Для одного типа ошибок, может быть несколько самих ошибок
#            [0]:'error message'
#            [1]:'error code'
#     TYPE_SECOND: # может быть несколько типов ошибок
#        [0]:
#            [0]:'error message'
#            [1]:'error code'
#
#

from .logger import Logger
from .errors.error_collection import ErrorCollection


class Response():

    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"

    DEFAULT_ERROR_CODE = 45689

    def __init__(self, answer=None):
        self.request_status = self.STATUS_SUCCESS
        self.request_errors = {}

        self.method_status = self.STATUS_SUCCESS
        self.method_result = None
        self.method_errors = {}

        self.logger = Logger.get_logger()

        if type(answer) is dict:
            self.load(answer)

    def dump(self):
        if self.has_request_error():
            return {
                "status": self.STATUS_ERROR,
                "errors": self.request_errors
            }
        else:
            return {
                "status": self.STATUS_SUCCESS,
                "answer": self._dump_method_answer()
            }

    def _dump_method_answer(self):
        if self.has_method_errors():
            return {
                "status": self.STATUS_ERROR,
                "errors": self.method_errors
            }
        else:
            return {
                "status": self.STATUS_SUCCESS,
                "result": self.method_result
            }

    def load(self, answer):
        self.logger.debug('Response: load answer:%s', answer)

        if 'status' not in answer:
            error_msg = "Answer must contains a 'status' key"
            self.logger.error('%s\n'
                              '  Answer:%s', error_msg, answer)
            raise StandardError("Answer must contains a 'status' key")

        self.request_status = answer['status']
        self.request_errors = answer.get("errors", {})

        self._load_method_result(answer)

    def _load_method_result(self, answer):
        if not self.has_request_error():
            if 'answer' not in answer:
                error_msg = "Answer must contains a 'answer' key"
                self.logger.error('%s\n'
                                  '  Answer:%s', error_msg, answer)
                raise StandardError(error_msg)

            method_answer = answer['answer']
            self.method_status = method_answer.get("status", self.STATUS_SUCCESS)
            self.method_errors = method_answer.get("errors", {})
            self.method_result = method_answer.get("result")

    def get_method_result(self):
        return self.method_result if not self.has_error() else None

    ################################################################################
    # Working under errors

    def has_error(self):
        return self.has_request_error() or self.has_method_errors()

    def has_request_error(self):
        return len(self.request_errors) > 0

    def has_method_errors(self):
        return len(self.method_errors) > 0

    def get_error(self):
        return self.get_request_error() or self.get_method_error()

    def get_request_error(self):
        return ErrorCollection.create_by_dict(self.request_errors) if self.has_request_error() else None

    def get_method_error(self):
        return ErrorCollection.create_by_dict(self.method_errors) if self.has_method_errors() else None

    ################################################################################
    # Добавление информации об ошибках

    def add_request_error(self, type_error, msg, code=None):
        if code is None:
            code = self.DEFAULT_ERROR_CODE

        if not isinstance(msg, basestring):
            self.logger.debug('Error msg is not a string. Representation it: %s', repr(msg))
            msg = repr(msg)

        self.request_status = self.STATUS_ERROR
        if type_error not in self.method_errors:
            self.request_errors[type_error] = [[msg, code]]
        else:
            self.request_errors[type_error].append([msg, code])

    def add_method_error(self, type_error, msg, code=None):
        if code is None:
            code = self.DEFAULT_ERROR_CODE

        if not isinstance(msg, basestring):
            self.logger.debug('Error msg is not a string. Representation it: %s', repr(msg))
            msg = repr(msg)

        self.method_status = self.STATUS_ERROR
        if type_error not in self.method_errors:
            self.method_errors[type_error] = [[msg, code]]
        else:
            self.method_errors[type_error].append([msg, code])
