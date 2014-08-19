# -*- coding: utf-8 -*-

from ..logger import Logger

from .types.error_unknown import ErrorUnknown
from .types.error_argument import ErrorArgument
from .types.error_bad_request import ErrorBadRequest
from .types.error_connection import ErrorConnection
from .types.error_in_action import ErrorAction


class ErrorConstructor():
    """
    Класс для создания классов ошибок.
    """

    TYPE_ERROR_UNKNOWN = ErrorUnknown.TYPE_DEFAULT
    TYPE_ERROR_BAD_REQUEST = ErrorBadRequest.TYPE_DEFAULT
    TYPE_ERROR_ARGUMENT = ErrorArgument.TYPE_DEFAULT
    TYPE_ERROR_CONNECTION = ErrorConnection.TYPE_DEFAULT
    TYPE_ERROR_IN_ACTION = ErrorAction.TYPE_DEFAULT


    CODE_ERROR_UNKNOWN = ErrorUnknown.CODE_DEFAULT
    CODE_ERROR_BAD_REQUEST = ErrorBadRequest.CODE_DEFAULT
    CODE_ERROR_ARGUMENT = ErrorArgument.CODE_DEFAULT
    CODE_ERROR_CONNECTION = ErrorConnection.CODE_DEFAULT
    CODE_ERROR_IN_ACTION = ErrorAction.CODE_DEFAULT

    def __init__(self):
        self.logger = Logger.get_logger()

    def create_by_dict(self, errors_dict):
        """
        Принимает ассоциативный массив ответа из Response
        Возвращает массив классов ошибок.

        Пример входного массива:
        {
            TYPE_FIRST: # Тип ошибки.
               [0]:
                   [0]:'error message'
                   [1]:'error code'

               [1]:     # Для одного типа ошибок, может быть несколько самих ошибок
                   [0]:'error message'
                   [1]:'error code'
            TYPE_SECOND: # может быть несколько типов ошибок
               [0]:
                   [0]:'error message'
                   [1]:'error code'
        }

        По историческим причинам, может так же прийти:
        {
            TYPE_FIRST: # Тип ошибки.
               [0]:
                   [0]:'error message'
                   [1]:'error message another'
                   [2]:'and third error'
        }

        """
        self.logger.debug('ErrorConstructor: create by dict: %s', repr(errors_dict))
        result = []

        for errors_type, errors_list_same_type in errors_dict.iteritems():
            for error in errors_list_same_type:
                obj = self.create_error_obj_by_type_and_property(errors_type, error)
                result.append(obj)

        return result

    def create_error_obj_by_type_and_property(self, error_type, errors):
        """
        :param error_type: тип ошибки
        :param errors: массив параметров ошибок. По умолчанию, предполагается что:
                            errors[0] - сообщение ошибки
                            errors[1] - код ошибки

                            Так же может прийти:
                            errors: string - сообщение ошибки

                            Но при желание эта структура может быть изменена и обработанна по особенному

        :type errors: list
        :return: объект ошибки
        """
        self.logger.debug('ErrorConstructor: create error by:\n  type: %s\n'
                          '  params: %s\n  type params: %s', repr(error_type), repr(errors), type(errors))

        if isinstance(errors, basestring):
            errors = [errors]

        if error_type == self.TYPE_ERROR_BAD_REQUEST:
            obj_result = ErrorBadRequest(*errors)
        elif error_type == self.TYPE_ERROR_ARGUMENT:
            obj_result = ErrorArgument(*errors)
        elif error_type == self.TYPE_ERROR_CONNECTION:
            obj_result = ErrorConnection(*errors)
        elif error_type == self.TYPE_ERROR_IN_ACTION:
            obj_result = ErrorAction(*errors)
        else:
            obj_result = ErrorUnknown(*errors)

        if hasattr(obj_result, 'set_type'):
            obj_result.set_type(error_type)
        return obj_result
