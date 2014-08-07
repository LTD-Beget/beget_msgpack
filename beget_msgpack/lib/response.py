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
# Структура данных при ошибке в запросе:
# status: 'error'
# answer:
#     status: 'error'
#     error:       # обратить внимание, что тут error в единственном числе
#         [0]:      # а тут может быть только одна ошибка
#             [0]:'error message'
#             [1]:'text message'
#


class Response():

    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"

    # Случайное число которое не встречается в проекте
    DEFAULT_ERROR_CODE = 45689

    # типы ошибок:
    REQUEST_ERROR_BAD_REQUEST = "BAD_REQUEST"   # неизвестный module.controller/action
    REQUEST_ERROR_TYPE_UNKNOWN = "UNKNOWN_ERROR_REQUEST"  # во всех остальных случаях

    METHOD_ERROR_TYPE_ARGUMENT = "ARGUMENT_ERROR"  # переданы неправильные аргументы
    METHOD_ERROR_TYPE_UNKNOWN = "UNKNOWN_ERROR"  # во всех остальных случаях

    def __init__(self, answer=None):
        self.request_status = self.STATUS_SUCCESS
        self.request_error = None

        self.method_status = self.STATUS_SUCCESS
        self.method_result = None
        self.method_errors = {}

        if type(answer) is dict:
            self.load(answer)

    def dump(self):
        if self.has_request_error():
            return {
                "status": self.request_status,
                "error": self.request_error
            }
        else:
            return {
                "status": self.request_status,
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
        if 'status' not in answer:
            raise StandardError("Answer must contains a 'status' key")

        self.request_status = answer['status']
        self.request_error = answer.get("error")

        self._load_method_result(answer)

    def _load_method_result(self, answer):
        if not self.has_request_error():
            if 'answer' not in answer:
                raise StandardError("Answer must contains a 'answer' key")

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
        return self.request_status == self.STATUS_ERROR

    def has_method_errors(self):
        return len(self.method_errors) > 0

    def get_error(self):
        return self.get_request_error() or self.get_method_error()

    def get_request_error(self):
        return self.request_error if self.has_request_error() else None

    def get_method_error(self):
        return self.method_errors if self.has_method_errors() else None

    def add_request_error(self, code, description):
        self.request_status = self.STATUS_ERROR
        self.request_error = code, description

    def add_method_error(self, type_error, msg, code=None):
        if code is None:
            code = self.DEFAULT_ERROR_CODE

        self.method_status = self.STATUS_ERROR
        if type_error not in self.method_errors:
            self.method_errors[type_error] = [[msg, code]]
        else:
            self.method_errors[type_error].append([msg, code])

