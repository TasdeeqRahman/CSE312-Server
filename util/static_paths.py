# from server import MyTCPHandler
import os

from util.request import Request
from util.response import Response

extension_to_mime_type : dict[str, str] = {
    "html": "text/html",
    "css": "text/css",
    "js": "text/javascript",
    "jpeg": "image/jpeg",
    "jpg": "image/jpg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "ico": "image/x-icon"
}

# This path is provided as an example of how to use the router
def static_paths(request : Request, handler):
    # this is the action for any path starting with "/public"
    # splice the path to get file to serve in Response
    # make sure to use the right MIME type from the file extension

    # find file to serve and MIME type
    # file_path : str = "/../" + request.path.removeprefix("/public/") # https://docs.python.org/3/library/stdtypes.html#str.removeprefix
    # extension : str = request.path.rsplit('.', 1)[-1] # https://docs.python.org/3/library/stdtypes.html#str.rsplit

    file_path = os.path.join(os.getcwd(), request.path[1:]) # https://docs.python.org/3/library/os.path.html#os.path.join

    if not os.path.exists(file_path): # https://docs.python.org/3/library/os.path.html#os.path.exists
        # respond with 404
        file_not_found = Response()
        file_not_found.set_status(404, "File not found")
        file_not_found.text("File not found")
        handler.request.send_response(file_not_found.to_data())

    # determine MIME type
    extension : str = os.path.splitext(file_path)[1].lstrip(".") # https://docs.python.org/3/library/stdtypes.html#bytes.lstrip
    mime_type : str = "text/plain; charset=utf-8"

    if extension in extension_to_mime_type:
        mime_type = extension_to_mime_type[extension]

    content_type : dict[str, str] = {
        "Content-Type": mime_type
    }

    # read bytes of the file
    with open(file_path, "rb") as fileObj:
        # send final response
        res = Response()
        res.headers(content_type)               # update Content-Type
        res.bytes(fileObj.read())               # read the file in binary
        handler.request.sendall(res.to_data())  # send bytes of response


