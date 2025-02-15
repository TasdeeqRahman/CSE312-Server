from util.response import Response


# test test test test test
# mjore test test test tes mroe test test test

# This path is provided as an example of how to use the router
def hello_path(request, handler):
    res = Response()
    res.text("hello")
    handler.request.sendall(res.to_data())
