#§ imports (to be cleaned up) §#

from flask import Blueprint, request, Response
import time
import json
import gzip

from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getLevelData, loadLevelListPage
from config.listConfig import LEVEL_LIST_TYPES, itemReturnLimit

#§ blueprint & route stuff §#
level_list_bp = Blueprint("level_list", __name__, url_prefix="/level")
@level_list_bp.route("/list", methods=["POST"])

#§ function §#

def list():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]:
        return errorResponse(validity["error"])
    
    #§ Grabbing current logged in user's internal ID §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()
    listType = request_data.get("type")
    index = int(request_data.get("index", 0))
    cursor = request_data.get("cursor")
    gamer_id = request_data.get("gamer_id")

    if listType not in LEVEL_LIST_TYPES:
        return errorResponse("invalid_list_type", 200)
    
    #§ Grabbing config for specific list type from user request §#
    # kelixe : as of now only 'own' and 'new' are supported
    
    listTypeConfig = LEVEL_LIST_TYPES[listType]
    if listType == "own":
        query = listTypeConfig["query"](gamer_id)
    else:
        query = listTypeConfig["query"]()
    cursor_field = listTypeConfig["cursor_field"]

    #§ Grabbing items, next cursor and allLoaded
    items, cursorToReturn, allLoaded = loadLevelListPage(query, cursor_field, cursor, itemReturnLimit)
    jsonLevelList = [getLevelData(u.internalId, loggedInId) for u in items]

    body = {
        "success": True,
        "result": {
            "all_loaded": allLoaded,
            "cursor": cursorToReturn,
            "index": index + len(items),
            "items": jsonLevelList
        },
        "updated": {},
        "timestamp": int(time.time())
    }
    return generateResponse(body)