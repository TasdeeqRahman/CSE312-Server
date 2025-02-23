import html
import json
import uuid

from util.request import Request
from util.response import Response
from util.database import chat_collection

def add_emoji(request : Request, handler) -> None:
    # action taken with a request.path that ends with an {messageID}
    # request content is JSON in form: {"emoji": "[emoji]"}
    # [emoji] is a single character string
    # users can add different emojis to the same message, but not with the same emoji multiple times (respond with 403)

    # decode JSON to get {"emoji": "[emoji]"}
    d: dict[str, str] = json.loads(request.body)
    emoji_to_add : str = d.get('emoji')

    # get user_id of user who made reaction
    user_id: str = request.cookies.get("session", "")
    if user_id == "":
        # this is user's first interaction with chat
        user_id = str(uuid.uuid4())

    # get message ID from the path
    message_id : str = request.path.rsplit("/", 1)[-1]

    # retrieve message being reacted to from chat collection
    message_to_react_to = chat_collection.find_one({"id": message_id})

    # maybe chance that message can't be found in the collection?

    curr_reactions : dict[str, list[str]] = message_to_react_to.get('reactions', {})
    if emoji_to_add not in curr_reactions:
        curr_reactions[emoji_to_add] = []

    # if user_id already reacted with the same emoji, 403 response
    if user_id in curr_reactions.get(emoji_to_add):
        already_reacted_response : Response = (Response()
                                               .set_status(403, "Forbidden")
                                               .text("reacting with same emoji as before"))
        handler.request.sendall(already_reacted_response.to_data())
        return

    # otherwise, add reaction to "reactions" field of the message in the database
    curr_reactions.get(emoji_to_add).append(user_id)
    chat_collection.update_one({"id": message_id}, {"$set": {
        "reactions": curr_reactions
    }})

    # send response
    res = (Response()
           .text("emoji added")
           .cookies({"session": user_id, "Max-Age": "3600"}))
    handler.request.sendall(res.to_data())
    return

def remove_emoji(request : Request, handler) -> None:


    # send response
    res = Response()
    handler.request.sendall(res.to_data())
    return

