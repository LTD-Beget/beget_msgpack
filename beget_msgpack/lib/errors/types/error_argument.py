# -*- coding: utf-8 -*-

from .base_error import BaseError


class ErrorArgument(BaseError):
    """
    Переданы некорректные аргументы
    """
    CODE_DEFAULT = 4
    TYPE_DEFAULT = "ARGUMENT_ERROR"
