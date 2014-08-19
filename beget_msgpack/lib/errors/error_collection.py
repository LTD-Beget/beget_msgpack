# -*- coding: utf-8 -*-

from .error_constructor import ErrorConstructor


class ErrorCollection():
    """
    Хранит в себе массив ошибок и предоставляет к ним доступ
    Позволяет:
        - Проходиться по ошибкам в foreach
        - При приведение коллекции к str, выводит текст первой ошибки
    """

    def __init__(self, errors):
        """
        :type errors: list[Exception]
        """
        assert isinstance(errors, list), 'errors in ErrorCollection must be in list'
        self.errors = errors
        self.current_index = 0

    def get_all(self):
        """Возвращаем массив ошибок"""
        return self.errors

    def __str__(self):
        # Если ошибок нет, то возвращаем пустой результат
        if not len(self.errors):
            return ''

        # Возвращаем текст первой ошибки
        error = self.errors[0]
        return str(error)

    def __iter__(self):
        # Возвращаем объект итератора
        return self

    def next(self):
        # Если вышли за пределы, то заканчиваем итерацию
        if len(self.errors) <= self.current_index:
            raise StopIteration

        # Возвращаем следующую ошибку и увеличиваем итератор
        self.current_index += 1
        return self.errors[self.current_index - 1]

    @classmethod
    def create_by_dict(cls, request_errors):
        error_constructor = ErrorConstructor()
        return cls(error_constructor.create_by_dict(request_errors))

