#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_emblem_data, load_emblem_list_page

from config import listConfig

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
emblem_ownList_bp = Blueprint("emblem_ownList", __name__, url_prefix="/emblem")
@emblem_ownList_bp.route("/ownList", methods=["POST"])

def ownList():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    index = int(requestData.get("index", 0))
    cursor = requestData.get("cursor")

    #§ Checking if request contains required paramaters §#
    if "index" not in requestData or "cursor" not in requestData:
        return error_response("missing_parameters")
    
    #§ Grabbing config for specific list type from user request §#
    listTypeConfig = listConfig["emblemListTypes"]["own"]
    query = listTypeConfig["query"](gamerId=loggedInId)
    cursor_field = listTypeConfig["cursor_field"]

    #§ Grabbing items, next cursor and allLoaded
    items, cursorToReturn, allLoaded = load_emblem_list_page(query, cursor_field, cursor, listConfig["itemReturnLimit"])
    jsonEmblemList = [get_emblem_data(u.internalId) for u in items]

    body = {
        "success": True,
        "result": {
            "all_loaded": allLoaded,
            "cursor": cursorToReturn,
            "index": index + len(items),
            "items": jsonEmblemList
        },
        "updated": {},
        "timestamp": int(time.time())
    }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)
