import json

from pymongo.response import Response

class Response:

    # example response from Week 2.1 Lecture Slides
    # HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nhello

    def __init__(self) -> None:
        # set defaults for:
        # http version, status code, status message
        # response headers
        # body
        self.http_version : str = "HTTP/1.1"
        self.status_code : int = 200
        self.status_message : str = "OK"

        # default Content-Type is "text/plain; charset=utf-8"
        # had to rename so not confused with the function .headers()
        self.final_headers : dict[str, str] = {
            "Content-Type" : "text/plain; charset=utf-8",
            "Content-Length" : "0",
            "X-Content-Type-Options": "nosniff" # Week 2.2 Slide 22
        }

        # had to rename bc naming conflicts
        self.final_cookies : dict[str, str] = {}
        self.body : bytes = b""

        # Set-Cookie ????

    def set_status(self, code : int, text : str) -> Response:
        # sets status code and message of response
        self.status_code : int = code
        self.status_message : str = text
        return self

    def headers(self, headers : dict[str, str]) -> Response:
        # adds/changes key-value pairs from dict as headers of response
        # handles all headers EXCEPT Set-Cookie
        self.final_headers.update(headers)
        return self

    def cookies(self, cookies : dict[str, str]) -> Response:
        # adds key-value pairs from dict as cookies of response
        # multiple calls has to maintain previous cookies
        self.final_cookies.update(cookies)

        # Week 2.3 Slides
        # responses can possibly involve multiple Set-Cookie headers
        # example:
        # Set-Cookie: id=X6kAwpgW29M
        # Set-Cookie: visits=4
        # Set-Cookie: id=X6kAwpgW29M; Expires=Wed, 7 Feb 2024 16:35:00 GMT
        # Set-Cookie: id=X6kAwpgW29M; Max-Age=3600
        # (cookie expires 1hr after being set
        # Set-Cookie: id=X6kAwpgW29M; Path=/posts

        # some aren't even in key-value pairs ("directives")
        # Set-Cookie: id=X6kAwpgW29M; Secure
        #  Set-Cookie: id=X6kAwpgW29M; HttpOnly

        return self

    def bytes(self, data : bytes) -> Response:
        # appends input to end of body of response as bytes
        self.body += data
        self.final_headers["Content-Length"] = str(len(self.body))
        return self

    def text(self, data : str) -> Response:
        # appends input to end of body of response as bytes
        # multiple calls maintains body
        self.body += data.encode("utf-8")
        self.final_headers["Content-Length"] = str(len(self.body))
        return self

    def json(self, data : dict | list) -> Response:
        # sets body of response to input converted to json as bytes
        # replaces old body always
        # sets Content-Type to "application/json"
        self.body : bytes = json.dumps(data).encode("utf-8")
        self.final_headers["Content-Type"] = "application/json"
        self.final_headers["Content-Length"] = str(len(self.body))
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
        for key, value in self.final_headers.items():
            new_header : bytes = ((key + ": " + value + "\r\n")
                                  .encode("utf-8"))
            headers += new_header

        # final header will always add a b"\r\n" to the end

        # if no cookies, will get final b"\r\n" automatically
        # if have cookies, need both \r\n's
        # Set-Cookie ???
        set_cookie_header : bytes = b"\r\n" # just to handle case where no cookies
        if len(self.final_cookies) > 0:
            set_cookie_header: bytes = b"Set-Cookie: "
            counter: int = 0
            for key, value in self.final_cookies.items():
                counter += 1

                if counter == len(self.final_cookies):
                    # means at last key-value pair, so don't add ";" to end
                    if key == "HttpOnly" or key == "Secure":
                        only_key : bytes = (key + "\r\n\r\n").encode("utf-8")
                        set_cookie_header += only_key
                    else:
                        key_value_pair : bytes = (key + ": " + value + "\r\n\r\n").encode("utf-8")
                        set_cookie_header += key_value_pair
                else:
                    # add space between key-value pairs
                    if key == "HttpOnly" or key == "Secure":
                        only_key : bytes = (key + "; ").encode("utf-8")
                        set_cookie_header += only_key
                    else:
                        key_value_pair : bytes = (key + ": " + value + "; ").encode("utf-8")
                        set_cookie_header += key_value_pair

        # add body
        return status_line + headers + set_cookie_header + self.body

def test1():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()
    print(actual)

def test2():
    res = Response()
    res.text("hello")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\nContent-Length: 5\r\n\r\nhello'
    actual = res.to_data()

    new_header : dict[str, str] = {
        "Content-Type" : "text/html",
    }
    res.headers(new_header)
    res.text("i am changing the body !@#$%^&)(*)(*&")
    actual = res.to_data()
    print(actual)

def test3():
    res = Response()
    res.text("")
    expected = b'HTTP/1.1 200 OK\r\nContent-Type: "text/html"\r\nContent-Length: 5\r\nSet-Cookie: HttpOnly; Secure\r\n\r\nhello'
    actual = res.to_data()

    new_header : dict[str, str] = {
        "Content-Type" : "text/html",
    }
    res.headers(new_header)

    new_cookies : dict[str, str] = {
        "HttpOnly" : "1",
        "Secure" : "1",
    }
    res.cookies(new_cookies)
    res.text("")
    actual = res.to_data()
    print(actual)

# add tests for actual key-value pairs for Cookies

if __name__ == '__main__':
    test1()
    test2()
    test3()

# Week 2.1 Slide 29: server can't handle a requested path\r\n
# b"HTTP/1.1 404 Not Found\r\n
# Content-Type: text/plain\r\n
# Content-Length: 36\r\n\r\n
# The requested content does not exist"
