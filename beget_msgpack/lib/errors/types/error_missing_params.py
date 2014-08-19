# -*- coding: utf-8 -*-

from .base_error import BaseError


class ErrorMissingParams(BaseError):
    """
    Ошибка непереданных или неправильных аргументов
    """

    CODE_DEFAULT = 7
    TYPE_DEFAULT = "MISSING_PARAMS"
