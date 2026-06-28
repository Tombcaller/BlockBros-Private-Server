#§ -------- IMPORTS -------- §#

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Emblem, db
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_emblem_data, get_player_data
from utils.db_item_factory import build_emblem

#§ Misc Imports §#
import time

#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
emblem_post_bp = Blueprint("emblem_post", __name__, url_prefix="/emblem")
@emblem_post_bp.route("/post", methods=["POST"])

def post():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Getting user's request data from Flask §#
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    title = requestData.get("title")
    desc = requestData.get("desc")
    emblemMap = requestData.get("map")

    #§ Returning error if any fields are missing §#
    if not title or not desc or not emblemMap:
        return {"error": "Invalid request"}, 400
    
    #§ Grabbing emblem object from build_emblem function §#
    newEmblem = build_emblem(title, desc, emblemMap, loggedInId)
    db.session.add(newEmblem)

    db.session.commit()

    #§ Grabbing emblem data from database to send back (Including new emblemId) §#
    result = get_emblem_data(newEmblem.emblemInternalId, loggedInId)

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": result,
        "updated": get_player_data(loggedInId,2),
        "timestamp": int(time.time())
        }
    
    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)