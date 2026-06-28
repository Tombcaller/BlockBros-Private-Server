#§ imports ------------------ §#
from flask import Blueprint, request

from models import Emblem, db
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_player_data

import time

try:
    from utils.get_db_data import get_player_data
except ImportError as e:
    print("Erreur import get_player_data:", e)

#§ ------------------------- §#

#§ bp and route§#
emblem_delete_bp = Blueprint("emblem_delete", __name__, url_prefix="/emblem")
@emblem_delete_bp.route("/delete", methods=["POST"])

def delete():
    #§ validity check§#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    
    #§ request data and batch processing §
    # #
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    #§ grabbing data if valid §#
    emblem_id = requestData.get("emblem_id")
    if not emblem_id:
        return error_response("missing_parameters")
    
    #§ deleting emblem from database after validation §#
    emblemEntry = db.session.query(Emblem).filter_by(emblemInternalId=emblem_id).first()

    if not emblemEntry:
        return error_response("emblem_not_found")

    if emblemEntry.creatorInternalId != int(loggedInId):
        return error_response("not_emblem_creator")
    
    db.session.delete(emblemEntry)
    db.session.commit()

    body = {
        "success": True,
        "result": {
            "id": emblem_id
        },
        "updated": get_player_data(loggedInId, 2),
        "timestamp": int(time.time())
    }

    return generate_response(body)