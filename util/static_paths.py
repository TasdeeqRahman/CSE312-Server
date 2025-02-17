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
def serve_static_file(request : Request, handler) -> None:
    # this is the action for any path starting with "/public"
    # splice the path to get file to serve in Response
    # make sure to use the right MIME type from the file extension

    ##################################
    # don't know how/when to send a 404

    # find file to serve and MIME type
    # file_path = os.path.join(os.getcwd(), request.path[1:]) # https://docs.python.org/3/library/os.path.html#os.path.join
    file_path = request.path[1:] # just get rid of the leading "/"

    # if not os.path.exists(file_path): # https://docs.python.org/3/library/os.path.html#os.path.exists
    #     # respond with 404
    #     file_not_found = Response()
    #     file_not_found.set_status(404, "File not found")
    #     file_not_found.text("File not found")
    #     handler.request.send_response(file_not_found.to_data())

    # chance for error if path is not to file but still valid

    # determine MIME type
    # extension : str = os.path.splitext(file_path)[1].lstrip(".") # https://docs.python.org/3/library/stdtypes.html#bytes.lstrip
    extension : str = request.path.rsplit('.', 1)[-1]  # https://docs.python.org/3/library/stdtypes.html#str.rsplit

    # unavoidable KeyError if path does not lead to file with extension
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

    return

def render_template(request : Request, handler, path_to_render : str) -> None:
    # read from template_path
    # read from layout.htmp
    # replace {{content}} with contents of template_path
    # send bytes through response
    with open(path_to_render, "rb") as fileObj:
        new_content : bytes = fileObj.read()

    template_path : str = "public/layout/layout.html"
    with open(template_path, "rb") as fileObj:
        to_replace : bytes = fileObj.read()

    # replace
    to_render : bytes = to_replace.replace(b"{{content}}", new_content)

    # send response
    res = Response()
    res.headers({
        "Content-Type": "text/html"
    })
    res.bytes(to_render)
    handler.request.sendall(res.to_data())
    return

def handle_index(request : Request, handler) -> None:
    render_template(request, handler, "public/index.html")
    return

def handle_chat(request : Request, handler) -> None:
    render_template(request, handler, "public/chat.html")
    return
