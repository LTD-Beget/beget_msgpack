# -*- coding: utf-8 -*-

from .base_error import BaseError


class ErrorAction(BaseError):
    """
    Ошибка при возникновение исключения в коде экшена.
    """

    CODE_DEFAULT = 6
    TYPE_DEFAULT = 'internal_error'   # В нижнем формате, для совместимости c константами в phportal.
