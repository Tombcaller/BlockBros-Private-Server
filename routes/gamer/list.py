#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getPlayerData, loadGamerListPage
from config.listConfig import GAMER_LIST_TYPES, itemReturnLimit

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_list_bp = Blueprint("gamer_list", __name__, url_prefix="/gamer")
@gamer_list_bp.route("/list", methods=["POST"])

def list():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]:
        return errorResponse(validity["error"])

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()
    listType = request_data.get("type")
    index = int(request_data.get("index", 0))
    cursor = request_data.get("cursor")

    #§ Checking if request contains required paramaters §#
    if not listType:
        return errorResponse("missing_parameters")

    #§ Checking if request contains valid paramaters §#
    if listType not in GAMER_LIST_TYPES:
        return errorResponse("invalid_list_type", 200)

    #§ Grabbing config for specific list type from user request §#
    listTypeConfig = GAMER_LIST_TYPES[listType]
    query = listTypeConfig["query"]()
    cursor_field = listTypeConfig["cursor_field"]

    #§ Grabbing items, next cursor and allLoaded
    items, cursorToReturn, allLoaded = loadGamerListPage(query, cursor_field, cursor, itemReturnLimit)
    jsonPlayerList = [getPlayerData(u.internalId) for u in items]

    body = {
        "success": True,
        "result": {
            "all_loaded": allLoaded,
            "cursor": cursorToReturn,
            "index": index + len(items),
            "items": jsonPlayerList
        },
        "updated": {},
        "timestamp": int(time.time())
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)
