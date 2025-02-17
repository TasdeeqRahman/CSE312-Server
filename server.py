import socketserver
from util.request import Request
from util.router import Router
from util.hello_path import hello_path
from util.static_paths import serve_static_file, handle_index, handle_chat
from util.for_chat import create_chat_message, retrieve_all_messages, update_chat_message, delete_chat_message


class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.router = Router()
        self.router.add_route("GET", "/hello", hello_path, True)
        # TODO: Add your routes here

        self.router.add_route("GET", "/public", serve_static_file, False)
        self.router.add_route("GET", "/", handle_index, True)
        self.router.add_route("GET", "/chat", handle_chat, True)

        self.router.add_route("POST", "/api/chats", create_chat_message, True)
        self.router.add_route("GET", "/api/chats", retrieve_all_messages, True)
        self.router.add_route("PATCH", "/api/chats", update_chat_message, False)
        self.router.add_route("DELETE", "/api/chats", delete_chat_message, False)

        super().__init__(request, client_address, server)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        self.router.route_request(request, self)


def main():
    host = "0.0.0.0"
    port = 8080
    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
