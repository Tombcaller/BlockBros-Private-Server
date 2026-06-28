#§ imports ------------------ §#
from flask import Blueprint, request

from models import db, Level
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_player_data

import time

#§ ------------------------- §#

#§ bp and route§#
level_delete_bp = Blueprint("level_delete", __name__, url_prefix="/level")
@level_delete_bp.route("/delete", methods=["POST"])

def delete():
    #§ validity check§#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    
    #§ request data and batch processing §#
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    #§ grabbing data if valid §#
    level_id = requestData.get("level_id")
    if not level_id:
        return error_response("missing_parameters")
    
    #§ deleting level from database after validation §#
    levelEntry = db.session.query(Level).filter_by(internalId=level_id).first()

    if not levelEntry:
        return error_response("level_not_found")

    if levelEntry.gamerInternalId != int(loggedInId):
        return error_response("not_level_creator")
    
    db.session.delete(levelEntry)
    db.session.commit()

    body = {
        "success": True,
        "result": {},
        "updated": get_player_data(loggedInId, 2),
        "timestamp": int(time.time())
    }

    return generate_response(body)