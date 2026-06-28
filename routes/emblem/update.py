#§ imports ------------------ §#
from flask import Blueprint, json, request

from models import Interactions, db, Emblem
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_emblem_data

import time

#§ ------------------------- §#

#§ bp and route§#
emblem_update_bp = Blueprint("emblem_update", __name__, url_prefix="/emblem")
@emblem_update_bp.route("/update", methods=["POST"])

def update():
    #§ validity check§#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    
    print("0")
    #§ request data and batch processing §#
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    print("FULL REQUEST DATA:", request.get_json())

    print("1")
    #§ grabbing data if valid §#
    emblemId = requestData.get("emblemId")
    print("emblemId:", emblemId)
    title = requestData.get("title")
    print("title:", title)
    desc = requestData.get("desc")
    print("desc:", desc)
    emblemMap = requestData.get("map")
    print("emblemMap")
    if not emblemId or not title or not desc or not emblemMap:
        return error_response("missing_parameters")

    print("2")
    #§ updating level in database§#
    emblemEntry = db.session.query(Emblem).filter_by(emblemInternalId=emblemId).first()
    if not emblemEntry:
        return error_response("emblem_not_found")
    if emblemEntry.creatorInternalId != int(loggedInId):
        return error_response("not_emblem_creator")
    emblemEntry.title = title
    emblemEntry.desc = desc
    emblemEntry.emblemMap = emblemMap
    db.session.commit()

    print("3")
    body = {
        "success": True,
        "result": get_emblem_data(emblemEntry.emblemInternalId),
        "updated": {},
        "timestamp": int(time.time())
    }

    return generate_response(body)