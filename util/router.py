from server import MyTCPHandler
from util.request import Request
from util.response import Response


# helper class to contain all needed information about a Route
class Route:
    def __init__(self, method : str, path : str, action, exact_path : bool = False) -> None:
        self.method : str = method
        self.path : str = path
        self.action = action # action : (Request, MyTCPHandler) -> None
        self.exact_path : bool = exact_path

class Router:

    def __init__(self) -> None:
        # if multiple routes match the request, have to
        # choose the first one that matches, so need a list
        self.routes : list[Route] = []

    def add_route(self, method : str, path : str, action, exact_path : bool = False) -> None:
        # action is a function that handles request matching the method and path
        # action : (Request, MyTCPHandler) -> None
        newRoute : Route = Route(method, path, action, exact_path)
        self.routes.append(newRoute)
        return

    def route_request(self, request : Request, handler : MyTCPHandler) -> None:
        # check the method and path of the request
        # determine "added route" to be used
        # call the function associated with that route with correct arguments
        # send 404 Not Found response otherwise

        # iterate through self.routes, until you find a matching Route object for the
        # requested method and path (have to consider exact_path too)
        # if you find a Route, call Route.action, otherwise send 404 Not Found
        for route in self.routes:
            if route.method == request.method: # do I have to worry about capitalization?
                if route.exact_path and route.path == request.path:
                    route.action(request, handler)
                    # action won't return anything, so prevent future iterations from running
                    return
                elif request.path.startswith(route.path):
                    route.action(request, handler)
                    return

        # if the appropriate action wasn't taken in the loop,
        # respond with a 404
        not_found_response : Response = Response()
        not_found_response.set_status(404, "Not Found")
        not_found_response.text("The requested content does not exist")
        handler.request.sendall(not_found_response.to_data())
        return
