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
        headers_and_body : list[bytes] = request.split(b'\r\n\r\n', 1)
        self.body : bytes = headers_and_body[1]

        # split headers on \r\n (surely \r\n cannot be used as a value to a header ?)
        headers : list[bytes] = headers_and_body[0].split(b'\r\n')

        # split the first line of the headers by the first 2 whitespaces
        # the three resulting parts is the method, path, and http_version
        # use split : https://docs.python.org/3/library/stdtypes.html#bytes.split
        request_line_parts : list[bytes] = (headers[0]
                                     .split(b' '))
        # looks like: [b"POST", b"/api/chats", b"HTTP/1.1"]

        # bytes to str : https://docs.python.org/3/library/stdtypes.html#bytes.decode
        self.method : str = request_line_parts[0].decode('utf-8')
        self.path : str = request_line_parts[1].decode('utf-8')
        self.http_version : str = request_line_parts[2].decode('utf-8')

        ####################################

        self.headers: dict[str, str] = {}
        self.cookies: dict[str, str] = {}

        # what headers look like:
        #  [b"Host: localhost:8080",
        #  b"Content-Type: application/json",
        #  b"Content-Length: 18",
        #  b"Cookie: id=123; theme=dark",
        #  b"Origin: http://localhost:8080"]

        # every subsequent line in headers:
        # retrieve content from after the :, left trim the whitespace, if it exists, and
        # populate the dictionary
        # if the header before the : is "Cookie", have to create a dictionary?
        for header in headers[1:]: # skip the request line
            # split on the 1st :, left trim the whitespace (if it exists) of second elemnt
            header_parts : list[bytes] = header.split(b':', 1)
            header_key : str = header_parts[0].decode('utf-8')
            header_value : str = (header_parts[1]
                                    .lstrip() # https://docs.python.org/3/library/stdtypes.html#bytes.lstrip
                                    .decode('utf-8'))

            # handle cookies
            # example header value: "id=123; theme=dark"
            if header_key == 'Cookie':
                # split by b';'
                # for every key-value pair, lstrip, split by "=", store in dict
                key_value_pairs : list[str] = header_value.split(';')
                for kv in key_value_pairs:
                    kv.lstrip()
                    key_and_value : list[str] = kv.split('=', 1)
                    self.cookies[key_and_value[0]] = key_and_value[1]

            self.headers[header_key] = header_value

def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    print("test1 passed")
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

if __name__ == '__main__':
    test1()
