
import logging
import uuid


class LoggerAdapterRequestId(logging.LoggerAdapter):

    static_global_request_id = None
    static_platform = 'pyportal'
    static_handler = 'msgpack'

    def __init__(self, logger, extra):
        super(LoggerAdapterRequestId, self).__init__(logger, extra)
        self.extra['platform'] = self.static_platform
        self.extra['handler'] = self.static_handler

    def request_id_generate(self):
        self.logger.request_id = str(uuid.uuid4())[:8]

    def request_id_clear(self):
        self.logger.request_id = ''

    def process(self, msg, kwargs):
        self.extra['global_request_id'] = self.static_global_request_id

        if 'extra' in kwargs.keys():
            kwargs['extra'].update(self.extra)
        else:
            kwargs['extra'] = self.extra

        if hasattr(self.logger, 'request_id') and self.logger.request_id:
            self.extra['request_id'] = self.logger.request_id
            return '[id:%s] %s' % (self.logger.request_id, msg), kwargs
        return msg, kwargs

    def set_global_request_id(self, global_id):
        """

        :param global_id:
        :return:
        """
        self.extra['global_request_id'] = global_id


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
