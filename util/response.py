import json


class Response:

    # this is something
    # this is something
    # this is something

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
