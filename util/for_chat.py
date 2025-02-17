import html
import json
import uuid

from util.request import Request
from util.response import Response
from util.database import chat_collection

class Message:
    def __init__(self, author : str, ident : str, content : str, updated : bool = False) -> None:
        self.author : str = author      # maps to session id for now
        self.identify : str = ident     # maps to message id
        self.content : str = content    # maps to message content
        self.updated : bool = updated   # w/e

    def get_message_document(self) -> dict[str, str]:
        ret : dict[str, str] = {
            "author" : self.author,
            "id" : self.identify,
            "content" : self.content,
            "updated" : self.updated,
        }
        return ret

# !!!!!!!!!!! must escape any HTML in users' messages

def create_chat_message(request : Request, handler) -> None:
    # body of the request will be JSON string (have to decode from {"content": string}
    # can assume it's properly formatted
    # 200 OK response, "message sent" message
    # name cookie "session", which will contain unique id that identifies users
    # set cookie when they type first message
    # randomly generated names through uuid package

    # decode json to get dict["content": str], escape html char's
    d : dict = json.loads(request.body)
    message_content : str = html.escape(d["content"])

    # cookies: either it has the cookie "session," or we need to give the new user one
    user_id : str = request.cookies.get("session", "")
    if user_id == "":
        # this is user's first message
        user_id = str(uuid.uuid4())

    # create id for message (uuid)
    message_id : str = str(uuid.uuid4())

    # store message id and author into database
    new_message : Message = Message(
        user_id,
        message_id,
        message_content
    )
    chat_collection.insert_one(new_message.get_message_document())

    # send response
    response : Response = Response()
    response.text("message sent")
    response.cookies({"session": user_id, "Max-Age": "3600"})
    handler.request.sendall(response.to_data())
    return

def retrieve_all_messages(request : Request, handler) -> None:
    # from a GET request
    # Response body is JSON : {"message": [{"author": string, "id": string, "content": string, "updated": boolean}, ...]}
    # "updated" represents if the message has even been updated

    # ret is a json dict with only one key-value pair, value being a list
    list_of_messages = []
    for message in chat_collection.find():
        list_of_messages.append({
            "author": message["author"],
            "id": message["id"],
            "content": message["content"],
            "updated": message["updated"],
        })

    response : Response = Response()
    response.json({"messages": list_of_messages})
    handler.request.sendall(response.to_data())
    return

def update_chat_message(request : Request, handler) -> None:
    # action taken with a request.path that ends with an {id}
    # Request body is JSON in format: {"content": string}
    # update the message, and then set the "updated" field to "True"
    # responds with 403 Forbidden when user lacks permission because not own message

    # retrieve user's identifying cookie
    user_id: str = request.cookies.get("session", "")
    if user_id == "":
        # user can't have permission to change
        no_permission_response : Response = (Response()
                                  .set_status(403, "Forbidden")
                                  .text("No session cookie found"))
        handler.request.sendall(no_permission_response.to_data())

    # retrieve {id} in path
    message_id : str = request.path.rsplit("/", 1)[-1]

    # find the message in the collection, and verify session id is the same
    chat_message_to_change = chat_collection.find_one({"id": message_id})

    if chat_message_to_change["author"] != user_id:
        # no permission to change because session id's don't match
        no_permission_response : Response = (Response()
                                  .set_status(403, "Forbidden")
                                  .text("Session cookie ID does not match owner"))
        handler.request.sendall(no_permission_response.to_data())

    # decode request body, and change contents of chat message
    d: dict = json.loads(request.body)
    message_content: str = html.escape(d["content"])

    # update the chat message
    chat_collection.update_one({"id": message_id}, {"$set":
                                                        {"content": message_content,
                                                         "updated": True}})

    # respond
    response : Response = (Response()
        .text("message updated")
        .cookies({
            "session": user_id,
            "Max-Age": "3600"
        }))
    handler.request.sendall(response.to_data())
    return


def delete_chat_message(request : Request, handler) -> None:
    # action taken with a request.path that ends with an {id}
    # responds with 403 Forbidden when user lacks permission because not own message
    # hard delete

    # copy update, but delete chat message instead
    # retrieve user's identifying cookie
    user_id: str = request.cookies.get("session", "")
    if user_id == "":
        # user can't have permission to delete
        no_permission_response : Response = (Response()
                                  .set_status(403, "Forbidden")
                                  .text("No session cookie found"))
        handler.request.sendall(no_permission_response.to_data())

    # retrieve {id} in path
    message_id: str = request.path.rsplit("/", 1)[-1]

    # find the message in the collection, and verify session id is the same
    chat_message_to_delete = chat_collection.find_one({"id": message_id})

    if chat_message_to_delete["author"] != user_id:
        # no permission to delete because session id's don't match
        no_permission_response : Response = (Response()
                                  .set_status(403, "Forbidden")
                                  .text("Session cookie ID does not match owner"))
        handler.request.sendall(no_permission_response.to_data())

    # delete the message
    chat_collection.delete_one({"id": message_id})

    # respond
    response : Response = (Response()
        .text("message deleted")
        .cookies({
            "session": user_id,
            "Max-Age": "3600"
        }))
    handler.request.sendall(response.to_data())
    return



