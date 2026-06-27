# imports --------------------- #
from flask import Blueprint, request

from models import db, Emblem
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_emblem_data, get_player_data

import time

# blueprint & route stuff ----- #
emblem_get_bp = Blueprint("emblem_get", __name__, url_prefix="/emblem")
@emblem_get_bp.route("/get", methods=["POST"])

def get():
    # good ol validity check
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    
    # grabbing current logged in user's internal ID
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()

    decode_batch(requestData.get("batch"), loggedInId)

    emblemId = requestData.get("refId")

    if not emblemId:
        return error_response("missing_parameters")

    emblemEntry = db.session.query(Emblem).filter(Emblem.emblemId == emblemId).first()
    if not emblemEntry:
        return error_response("emblem not found ") 
    
    emblemData = get_emblem_data(emblemEntry.internalId, loggedInId)
    if not emblemData:
        return error_response("emblem not found")
    
    gamerData = get_player_data(loggedInId)

    body = {
        "success": True,
        "result": {
            "emblem": emblemData,
            "gamer": gamerData
        },
        "updated": {},
        "timestamp": int(time.time())
    }

    print(body)
    return generate_response(body)