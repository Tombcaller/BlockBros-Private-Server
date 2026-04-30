# imports --------------------- #
from flask import Blueprint, request

from models import db, Level, Account
from utils.db_item_factory import build_completion
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getLevelData, getPlayerData

import time
from random import randint
from config.submaster import clearRewardList


# blueprint & route stuff ----- #
level_get_bp = Blueprint("level_get", __name__, url_prefix="/level")
@level_get_bp.route("/get", methods=["POST"])

def get():
    # good ol validity check
    validity = checkRequestValidity(request)
    if not validity["success"]:
        return errorResponse(validity["error"])
    
    # grabbing current logged in user's internal ID
    loggedInId = request.headers.get("Authorization").split(":")[0]

    request_data = request.get_json()
    level_id = request_data.get("level_id")

    levelEntry = db.session.query(Level).filter(Level.levelId == level_id).first()
    if not levelEntry:
        return errorResponse("level not found") 
    levelData = getLevelData(levelEntry.internalId, loggedInId)
    if not levelData:
        return errorResponse("level not found")
    
    body = {
        "success": True,
        "result": levelData,
        "updated": {},
        "timestamp": int(time.time())
    }
    return generateResponse(levelData)