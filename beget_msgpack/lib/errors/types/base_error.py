# -*- coding: utf-8 -*-


class BaseError(Exception):
    """
    Базовая ошибка которую рекомендуется наследовать.
    Сама ошибка не должна вызываться.
    """

    # Эти константы рекомендуется переопредилить в каждом из классов и разместить в ErrorConstructor
    TYPE_DEFAULT = 'BASE_ERROR'
    CODE_DEFAULT = 1

    def __init__(self, message, code=None):
        self.message = message
        self.code = code if code else self.CODE_DEFAULT
        self.type = self.TYPE_DEFAULT

    def set_type(self, error_type):
        """
        :type error_type: basestring
        :param error_type: имя типа ошибки
        """
        self.type = error_type

    def get_type(self):
        """
        :rtype: basestring
        """
        return self.type

    def __str__(self):
        return str(self.message)

    def __repr__(self):
        return str(self.__class__)
