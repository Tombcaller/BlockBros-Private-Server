#§ imports (to be cleaned up) §#

from flask import Blueprint, request
import time

from models import Interactions, Level
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_level_data, get_player_data, load_ranking_list_page
from config import listConfig

#§ blueprint & route stuff §#
level_ranking_list_bp = Blueprint("level_ranking_list", __name__, url_prefix="/level")
@level_ranking_list_bp.route("/ranking/list", methods=["POST"])

def list():
    print("called?")
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])

    #§ Getting user's request data from Flask §#
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    level_id = requestData.get("level_id")
    index = int(requestData.get("index", 0))
    cursor = requestData.get("cursor")

    #§ checking if level exists §#
    level = Level.query.filter_by(internalId=level_id).first()
    if not level:
        return error_response("level_not_found")
    
    query = Interactions.query.filter(Interactions.levelInternalId == level_id,Interactions.completionTime > 0).order_by(Interactions.completionTime.asc())

    #§ Grabbing items, next cursor and allLoaded
    items, cursorToReturn, allLoaded = load_ranking_list_page(query, "completionTime", cursor, 20)

    ranking_items = []
    for interaction in items:
        gamer_data = get_player_data(interaction.gamerInternalId, 2)
        ranking_items.append({
            "gamer": gamer_data,
            "time": interaction.completionTime
        })
    print("test")
    body = {
        "success": True,
        "result": {
            "all_loaded": allLoaded,
            "cursor": cursorToReturn,
            "index": index + len(items),
            "items": ranking_items
        },
        "updated": {},
        "timestamp": int(time.time())
    }
    return generate_response(body)