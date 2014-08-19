# -*- coding: utf-8 -*-

from .lib.msgpack.request import Request as MsgpackRequest
from .lib.fastcgi.request import Request as FcgiRequest
from .lib.logger import Logger


class RequestFactory:

    TYPE_FCGI = 'fcgi'
    TYPE_MSGPACK = 'msgpack'

    def __init__(self, config):
        self.config = config
        self.logger = Logger.get_logger()

    def get_request(self, server_name):
        """
        В зависимости от имени сервера и его конфига, возвращаем ему соответствующий класс запроса.
        """
        self.logger.debug('RequestFactory: get_request for server: %s', server_name)

        # проверяем конфиг на наличие настроек для сервера или настроект по умолчанию
        if server_name in self.config.servers:
            self.logger.debug('RequestFactory: find server in config')
            server_config = self.config.servers[server_name]
        elif 'default' in self.config.servers:
            self.logger.debug('RequestFactory: not find server in config')
            server_config = self.config.servers['default']
        else:
            error_msg = 'RequestFactory: don`t have config for %s or default' % server_name
            self.logger.critical(error_msg)
            raise ConfigError(error_msg)

        # Определяем адресс для подключения
        if 'host' in server_config:
            host = server_config['host']
        else:
            host = server_name
        self.logger.debug('RequestFactory: host for connect: %s', host)

        # Возвращаем класс запроса в зависимости от полученных настроек
        if server_config['type'] == self.TYPE_FCGI:
            if not 'port' in server_config:
                error_msg = 'RequestFactory: For fcgi connection, you must set "port" in config'
                self.logger.critical(error_msg)
                raise ConfigError(error_msg)
            if not 'script_dir' in server_config:
                error_msg = 'RequestFactory: For fcgi connection, you must set "script_dir" in config'
                self.logger.critical(error_msg)
                raise ConfigError(error_msg)
            if not 'script_name' in server_config:
                error_msg = 'RequestFactory: For fcgi connection, you must set "script_name" in config'
                self.logger.critical(error_msg)
                raise ConfigError(error_msg)
            if not 'secret' in server_config:
                error_msg = 'RequestFactory: For fcgi connection, you must set "secret" in config'
                self.logger.critical(error_msg)
                raise ConfigError(error_msg)
            self.logger.debug('RequestFactory: return fcgi request')

            return FcgiRequest(host,
                               server_config['port'],
                               server_config['script_dir'],
                               server_config['script_name'],
                               server_config['secret'])

        elif server_config['type'] == self.TYPE_MSGPACK:
            if not 'port' in server_config:
                error_msg = 'RequestFactory: For msgpack connection, you must set "port" in config'
                self.logger.critical(error_msg)
                raise ConfigError(error_msg)
            self.logger.debug('RequestFactory: return msgpack request')

            return MsgpackRequest(host, server_config['port'])

        else:
            error_msg = 'RequestFactory: don`t have information about type connection for server'
            self.logger.error(error_msg)
            raise ConfigError(error_msg)


# Custom Exceptions:

class ConfigError(Exception):
    pass
