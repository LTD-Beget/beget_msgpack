# -*- coding: utf-8 -*-

from .lib.response import Response


class ResponseFactory:
    """
    Класс для конструкции одного Response из разнообразных форматов:

        метод получения Response из чеголибо:
            Получаем исходный ответ чеголибо
            При необходимости декадируем его чтобы привести его к понятном для Request виду
            После получения утвержденного формата сообщения, передаем его в Request и возвращаем клиенту
    """

    def __init__(self):
        pass

    def get_response_by_msgpack_answer(self, answer):
        return Response(answer)

    def get_response_by_fcgi_answer(self, answer):
        return Response(answer)

    def get_response_by_request_error(self, code=None, description=None):
        response = Response()
        response.add_request_error(code, description)
