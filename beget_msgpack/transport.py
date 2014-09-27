# -*- coding: utf-8 -*-

from request_factory import RequestFactory


class Transport:
    """
    Задача:
      - Поддерживать принятый формат отправки сообщения.
    """

    def __init__(self, config):
        self.request_factory = RequestFactory(config)

    def send(self, path, params):
        """
        Отпрака сообщения

        :param path: принимаемый формат: 'server/controller/action'
        :type path: str

        :param params: аргументы передаваемые в экшен.
        :type params: dict
        """
        server, controller, action = path.split('/')
        request = self.request_factory.get_request(server)
        controller_action_path = controller + '/' + action
        request.request(controller_action_path, **params)
