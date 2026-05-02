#§ imports (to be cleaned up) §#

from flask import Blueprint, request
import time

from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_level_data, load_level_list_page
#from config.listConfig import LEVEL_LIST_TYPES, itemReturnLimit
from config import listConfig

#§ blueprint & route stuff §#
level_list_bp = Blueprint("level_list", __name__, url_prefix="/level")
@level_list_bp.route("/list", methods=["POST"])

def list():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])

    #§ Getting user's request data from Flask §#
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    listType = requestData.get("type")
    index = int(requestData.get("index", 0))
    cursor = requestData.get("cursor")
    gamerId = requestData.get("gamer_id")

    if listType not in listConfig["levelListTypes"]:
        return error_response("invalid_list_type", 200)
    
    #§ Grabbing config for specific list type from user request §#
    # kelixe : as of now only 'own' and 'new' are supported
    
    listTypeConfig = listConfig["levelListTypes"][listType]
    if listType == "own":
        query = listTypeConfig["query"](gamerId)
    else:
        query = listTypeConfig["query"]()
    cursor_field = listTypeConfig["cursor_field"]

    #§ Grabbing items, next cursor and allLoaded
    items, cursorToReturn, allLoaded = load_level_list_page(query, cursor_field, cursor, listConfig["itemReturnLimit"])
    jsonLevelList = [get_level_data(u.internalId, loggedInId) for u in items]

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
    return generate_response(body)