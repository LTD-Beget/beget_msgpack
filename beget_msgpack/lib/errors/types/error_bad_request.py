# -*- coding: utf-8 -*-

from .base_error import BaseError


class ErrorBadRequest(BaseError):
    """
    Неправильный запрос (имя контроллера, экшена)
    """

    CODE_DEFAULT = 3
    TYPE_DEFAULT = 'method_not_found'  # В нижнем формате, для совместимости c константами в phportal.
