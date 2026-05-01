#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_player_data, loadGamerListPage
#from config.listConfig import GAMER_LIST_TYPES, itemReturnLimit
from config import listConfig

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_list_bp = Blueprint("gamer_list", __name__, url_prefix="/gamer")
@gamer_list_bp.route("/list", methods=["POST"])

def list():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()
    listType = requestData.get("type")
    index = int(requestData.get("index", 0))
    cursor = requestData.get("cursor")

    #§ Checking if request contains required paramaters §#
    if not listType:
        return error_response("missing_parameters")

    #§ Checking if request contains valid paramaters §#
    if listType not in listConfig["gamerListTypes"]:
        return error_response("invalid_list_type", 200)

    #§ Grabbing config for specific list type from user request §#
    listTypeConfig = listConfig["gamerListTypes"][listType]
    query = listTypeConfig["query"]()
    cursor_field = listTypeConfig["cursor_field"]

    #§ Grabbing items, next cursor and allLoaded
    items, cursorToReturn, allLoaded = loadGamerListPage(query, cursor_field, cursor, listConfig["itemReturnLimit"])
    jsonPlayerList = [get_player_data(u.internalId) for u in items]

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

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)
