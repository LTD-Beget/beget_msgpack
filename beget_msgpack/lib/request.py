
from response import Response
import msgpackrpc


class Request(object):
    def __init__(self, host):
        self.host = host

    def request(self, route, **kwargs):

        if len(route.split("/")) != 2:
            raise StandardError("Route must be in 'controller/action' format")

        response = Response()

        try:
            client = msgpackrpc.Client(msgpackrpc.Address(self.host, 40105))
            answer = client.call(route, kwargs)
            response.load(answer=answer)
        except Exception as e:
            response.add_request_error(code="transport_error", description=str(e))

        return response

    @staticmethod
    def get_request(host):
        return Request(host)

