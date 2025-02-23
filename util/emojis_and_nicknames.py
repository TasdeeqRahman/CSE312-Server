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
    # action taken with a request.path that ends with an {messageID}
    # request content is JSON in form: {"emoji": "[emoji]"}
    # [emoji] is a single character string
    # cannot remove emoji user have not reacted with (respond with 403)

    # decode JSON to get {"emoji": "[emoji]"}
    d: dict[str, str] = json.loads(request.body)
    emoji_to_remove : str = d.get('emoji')

    # get user_id of user who wants to remove reaction
    user_id: str = request.cookies.get("session", "")
    if user_id == "":
        # every reaction should have an associated user_id, so this should not be possible
        # 404 response
        user_not_found_response : Response = (Response()
                                                    .set_status(404, "Not Found")
                                                    .text("User ID not found"))
        handler.request.sendall(user_not_found_response.to_data())
        return

    # get message ID from the path
    message_id: str = request.path.rsplit("/", 1)[-1]

    # retrieve message from chat collection
    message_to_remove_from = chat_collection.find_one({"id": message_id})

    # maybe chance that message can't be found in the collection?

    curr_reactions: dict[str, list[str]] = message_to_remove_from.get('reactions', {})
    if emoji_to_remove not in curr_reactions:
        # 403 response
        no_reaction_to_remove_response: Response = (Response()
                                                    .set_status(403, "Forbidden")
                                                    .text("trying to remove a reaction that doesn't exist"))
        handler.request.sendall(no_reaction_to_remove_response.to_data())
        return

    # if user_id already reacted with the same emoji, 403 response
    if user_id not in curr_reactions.get(emoji_to_remove, []):
        no_reaction_to_remove_response: Response = (Response()
                                              .set_status(403, "Forbidden")
                                              .text("trying to remove a reaction that doesn't exist"))
        handler.request.sendall(no_reaction_to_remove_response.to_data())
        return

    # otherwise, remove reaction from "reactions" field of the message in the database
    curr_reactions.get(emoji_to_remove).remove(user_id)

    # *** removing a user_id might remove the emoji entirely as a key
    if len(curr_reactions.get(emoji_to_remove, [])) == 0:
        del curr_reactions[emoji_to_remove]

    chat_collection.update_one({"id": message_id}, {"$set": {
        "reactions": curr_reactions
    }})

    # send response
    res = (Response()
           .text("emoji removed")
           .cookies({"session": user_id, "Max-Age": "3600"}))
    handler.request.sendall(res.to_data())
    return

def change_nickname(request : Request, handler) -> None:
    # request content is JSON in form: {"nickname": "[new nickname]"}
    # new  nicknames will add a "nickname" field for the user and all their messages

    # get new nickname from request body
    d : dict[str, str] = json.loads(request.body)
    new_nickname : str = d.get('nickname')

    # get user_id of user who made nickname change request
    user_id : str = request.cookies.get("session", "")
    if user_id == "":
        # this is user's first interaction with chat
        user_id = str(uuid.uuid4())

    # make changes to the chat collection
    # does this work if "nickname" isn't an existing field?
    chat_collection.update_many({"id": user_id}, {"$set": {
        "nickname": new_nickname
    }})

    # send response
    res = (Response()
           .text("nickname changed and database updated")
           .cookies({"session": user_id, "Max-Age": "3600"}))
    handler.request.sendall(res.to_data())
    return


