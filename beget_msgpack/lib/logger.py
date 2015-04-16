
import logging
import uuid


class LoggerAdapterRequestId(logging.LoggerAdapter):

    def request_id_generate(self):
        self.extra = {'request_id': str(uuid.uuid4())[:8]}

    def request_id_clear(self):
        self.extra = {'request_id': ''}

    def process(self, msg, kwargs):
        if self.extra['request_id']:
            return '[id:%s] %s' % (self.extra['request_id'], msg), kwargs

        return msg, kwargs


class Logger():

    logger_name = 'beget.msgpack'

    def __init__(self):
        pass

    @staticmethod
    def set_logger_name(name):
        Logger.logger_name = name

    @staticmethod
    def get_logger_name():
        return Logger.logger_name

    @staticmethod
    def get_logger(name=None):
        if name:
            Logger.set_logger_name(name)

        return LoggerAdapterRequestId(logging.getLogger(Logger.get_logger_name()), {'request_id': ''})
