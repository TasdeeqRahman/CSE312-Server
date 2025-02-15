import json


class Response:

    # example response from Week 2.1 Lecture Slides
    # HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nhello

    # response = headers + \r\n + body
    # headers = first line + rest of the lines
    # first line = http_version + status code + status message (with spaces)
    # rest of the lines:
        # go through every header + ": " + content for that header (don't know how to handle directives)

    def __init__(self):
        pass

    def set_status(self, code, text):
        pass

    def headers(self, headers):
        pass

    def cookies(self, cookies):
        pass

    def bytes(self, data):
        pass

    def text(self, data):
        pass

    def json(self, data):
        pass

    def to_data(self):
        return b''


def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()

if __name__ == '__main__':
    test1()
