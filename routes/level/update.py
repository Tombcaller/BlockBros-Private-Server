#§ imports ------------------ §#
from flask import Blueprint, request

from models import Interactions, db, Level
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_level_data

import time

#§ ------------------------- §#

#§ bp and route§#
level_update_bp = Blueprint("level_update", __name__, url_prefix="/level")
@level_update_bp.route("/update", methods=["POST"])

def update():
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
    title = requestData.get("title")
    map = requestData.get("map")
    theme = requestData.get("theme")
    clear_ranking = requestData.get("clear_ranking")
    level_group_id = requestData.get("level_group_id")
    config = requestData.get("config")
    if not level_id or not title or not map or not theme or not clear_ranking or level_group_id is None:
        return error_response("missing_parameters")
    
    #§ updating level in database§#
    levelEntry = db.session.query(Level).filter_by(internalId=level_id).first()
    if not levelEntry:
        return error_response("level_not_found")
    if levelEntry.gamerInternalId != loggedInId:
        return error_response("not_level_creator")
    levelEntry.title = title
    levelEntry.map = map
    levelEntry.theme = theme
    if config is not None:
        levelEntry.config = config
    levelEntry.version = (levelEntry.version or 0) + 1
    if clear_ranking == 1:
        db.session.query(Interactions).filter_by(levelInternalId=level_id).delete()
    db.session.commit()

    body = {
        "success": True,
        "result": {},
        "updated": get_level_data(levelEntry.internalId, loggedInId),
        "timestamp": int(time.time())
    }

    return generate_response(body)