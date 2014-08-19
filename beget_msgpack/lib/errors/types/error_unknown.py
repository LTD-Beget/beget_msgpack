
from .base_error import BaseError


class ErrorUnknown(BaseError):

    CODE_DEFAULT = 5
    TYPE_DEFAULT = 'UNKNOWN_ERROR'
