# imports --------------------- #
from flask import Blueprint, request

from models import db, Level
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import getLevelData

import time

# blueprint & route stuff ----- #
level_get_bp = Blueprint("level_get", __name__, url_prefix="/level")
@level_get_bp.route("/get", methods=["POST"])

def get():
    # good ol validity check
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    
    # grabbing current logged in user's internal ID
    loggedInId = request.headers.get("Authorization").split(":")[0]

    requestData = request.get_json()
    levelId = requestData.get("levelId")

    if not levelId:
        return error_response("missing_parameters")

    levelEntry = db.session.query(Level).filter(Level.levelId == levelId).first()
    if not levelEntry:
        return error_response("level not found") 
    levelData = getLevelData(levelEntry.internalId, loggedInId)
    if not levelData:
        return error_response("level not found")
    
    body = {
        "success": True,
        "result": levelData,
        "updated": {},
        "timestamp": int(time.time())
    }
    return generate_response(levelData)