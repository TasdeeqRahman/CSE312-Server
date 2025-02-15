# from server import MyTCPHandler
from util.request import Request
from util.response import Response

# This path is provided as an example of how to use the router
def hello_path(request : Request, handler):
    res = Response()
    res.text("hello")
    handler.request.sendall(res.to_data())
