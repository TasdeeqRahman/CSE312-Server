import json

from pymongo.response import Response


class Response:

    def __init__(self) -> None:
        # set defaults for:
        # http version, status code, status message
        # response headers
        # body
        self.http_version : str = "HTTP/1.1"
        self.status_code : int = 200
        self.status_message : str = "OK"

        # default Content-Type is "text/plain; charset=utf-8"
        self.headers : dict[str, str] = {
            "Content-Type" : "text/plain; charset=utf-8",
            "Content-Length" : "0",
            "X-Content-Type-Options": "nosniff" # Week 2.2 Slide 22
        }
        self.cookies : dict[str, str] = {}
        self.body : bytes = b""

        # Set-Cookie ????

    def set_status(self, code : int, text : str) -> Response:
        # sets status code and message of response
        self.status_code : int = code
        self.status_message : str = text
        return self

    def headers(self, headers : dict[str, str]) -> Response:
        # adds/changes key-value pairs from dict as headers of response
        self.headers.update(headers)
        return self

    def cookies(self, cookies : dict[str, str]) -> Response:
        # adds key-value pairs from dict as cookies of response
        # multiple calls has to maintain previous cookies
        self.cookies.update(cookies)
        return self

    def bytes(self, data : bytes) -> Response:
        # appends input to end of body of response as bytes
        self.body += data
        self.headers["Content-Length"] = str(len(self.body))
        return self

    def text(self, data : str) -> Response:
        # appends input to end of body of response as bytes
        # multiple calls maintains body
        self.body += data.encode("utf-8")
        self.headers["Content-Length"] = str(len(self.body))
        return self

    def json(self, data : dict | list) -> Response:
        # sets body of response to input converted to json as bytes
        # replaces old body always
        # sets Content-Type to "application/json"
        self.body = json.dumps(data).encode("utf-8")
        self.headers["Content-Type"] = "application/json"
        self.headers["Content-Length"] = str(len(self.body))
        return self

    def to_data(self) -> bytes:
        # contains entire response, properly formatted by HTTP
        # all headers, cookies, status code, status message, body, and Content-Length header
        # returned bytes might have additional headers

        # example response from Week 2.1 Lecture Slides
        # HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nhello

        # response = headers + \r\n + body

        # headers = first line (status line) + rest of the lines
        # first line = http_version + status code + status message (with spaces)
        status_line : bytes = (("" +
                                self.http_version +
                                " " +
                                str(self.status_code) +
                                " " +
                                self.status_message +
                                "\r\n")
                               .encode("utf-8"))

        # rest of the headers:
        # go through every header + ": " + content for that header (don't know how to handle directives)
        headers : bytes = b""
        for key, value in self.headers.items():
            new_header : bytes = ((key + ": " + value + "\r\n")
                                  .encode("utf-8"))
            headers += new_header

        # \r\n\r\n
        # add body
        return status_line + headers + b"\r\n\r\n" + self.body

def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()

if __name__ == '__main__':
    test1()
