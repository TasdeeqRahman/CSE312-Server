class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        #  example request from Week 3 Recitation slides:
        #  b“POST /api/chats HTTP/1.1\r\n
        #  Host: localhost:8080\r\n
        #  Content-Type: application/json\r\n
        #  Content-Length: 18\r\n
        #  Cookie: id=123; theme=dark\r\n
        #  Origin: http://localhost:8080\r\n
        #  \r\n
        #  {"content":"asdf"}”

        # split on the first \r\n\r\n => first part is headers, second is body
        # split headers on \r\n (surely \r\n cannot be used as a value to a header ?)
        # split the first line of the headers by the first 2 whitespaces
            # the three resulting parts is the method, path, and http_version
        # every subsequent line in headers:
            # retrieve content from after the :, left trim the whitespace, if it exists, and
            # populate the dictionary
            # if the header before the : is "Cookie", have to create a dictionary?

        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {}
        self.cookies = {}

def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

if __name__ == '__main__':
    test1()
