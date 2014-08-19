# -*- coding: utf-8 -*-

from .lib.response import Response
import msgpack
from .lib.logger import Logger


class ResponseFactory:
    """
    Класс для конструкции одного Response из разнообразных форматов:

        метод получения Response из чеголибо:
            Получаем исходный ответ чеголибо
            При необходимости декадируем его чтобы привести его к понятном для Request виду
            После получения утвержденного формата сообщения, передаем его в Request и возвращаем клиенту
    """

    def __init__(self):
        self.logger = Logger.get_logger()
        pass

    def get_response_by_msgpack_answer(self, answer):
        self.logger.debug('ResponseFactory->by_msgpack: get answer: %s', answer)
        return Response(answer)

    def get_response_by_fcgi_answer(self, answer):
        self.logger.debug('ResponseFactory->by_fcgi: get answer: %s', repr(answer))
        code, header, raw_answer, error = answer
        answer_unpack = msgpack.unpackb(raw_answer)
        self.logger.debug('ResponseFactory->by_fcgi: change it to: %s', repr(answer_unpack))
        return Response(answer_unpack)

    def get_response_by_request_error(self, type_error=None, message=None, code=None):
        self.logger.debug('ResponseFactory->by_request_error: get code: %s, description: %s',
                          repr(code),
                          repr(message))
        response = Response()
        response.add_request_error(type_error, message, code)
        return response
