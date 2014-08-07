import msgpackrpc
import beget_msgpack


class Request(object):
    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)

    def request(self, route, **kwargs):

        if len(route.split("/")) != 2:
            raise StandardError("Route must be in 'controller/action' format")

        response_factory = beget_msgpack.ResponseFactory()

        try:
            client = msgpackrpc.Client(msgpackrpc.Address(self.host, self.port))
            answer = client.call(route, kwargs)
            response = response_factory.get_response_by_msgpack_answer(answer)
        except Exception as e:
            response = response_factory.get_response_by_request_error(description=str(e))

        return response