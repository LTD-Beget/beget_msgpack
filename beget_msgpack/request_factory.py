# -*- coding: utf-8 -*-

from .lib.msgpack.request import Request as MsgpackRequest
from .lib.fastcgi.request import Request as FcgiRequest


class RequestFactory:

    TYPE_FCGI = 'fcgi'
    TYPE_MSGPACK = 'msgpack'

    def __init__(self, config):
        self.config = config

    def get_request(self, server_name):
        """
        В зависимости от имени сервера и его конфига, возвращаем ему соответствующий класс запроса.
        """

        # проверяем конфиг на наличие настроек для сервера или настроект по умолчанию
        if server_name in self.config.servers:
            server_config = self.config.servers[server_name]
        elif 'default' in self.config.servers:
            server_config = self.config.servers['default']
        else:
            raise ConfigError('don`t have config for %s or default')

        # Определяем адресс для подключения
        if 'host' in server_config:
            host = server_config['host']
        else:
            host = server_name

        # Возвращаем класс запроса в зависимости от полученных настроек
        if server_config['type'] == self.TYPE_FCGI:
            if not 'port' in server_config:
                raise ConfigError('For fcgi connection, you must set "port" in config')
            if not 'script_dir' in server_config:
                raise ConfigError('For fcgi connection, you must set "script_dir" in config')
            if not 'script_name' in server_config:
                raise ConfigError('For fcgi connection, you must set "script_name" in config')
            if not 'secret' in server_config:
                raise ConfigError('For fcgi connection, you must set "secret" in config')
            return FcgiRequest(host,
                               server_config['port'],
                               server_config['script_dir'],
                               server_config['script_name'],
                               server_config['secret'])

        elif server_config['type'] == self.TYPE_MSGPACK:
            return MsgpackRequest(host, server_config['port'])

        else:
            raise ConfigError('don`t have information about type connection for server')


# Custom Exceptions:

class ConfigError(Exception):
    pass
