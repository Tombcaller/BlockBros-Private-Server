#§ -------- IMPORTS -------- §#

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Account, db
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getLevelData, getPlayerData
from utils.db_item_factory import build_level

#§ Misc Imports §#
import time

#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
level_post_bp = Blueprint("level_post", __name__, url_prefix="/level")
@level_post_bp.route("/post", methods=["POST"])

def post():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]: 
        return errorResponse(validity["error"])

    #§ Grabbing current logged in user's internal ID §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    title = request_data["title"]
    levelMap = request_data["map"]
    theme = request_data["theme"]
    levelTime = request_data["time"]
    config = request_data["config"]

    #§ Returning error if any fields are missing §#
    if not title or not levelMap or not theme or not levelTime:
        return {"error": "Invalid request"}, 400
    
    #§ Grabbing level object from build_level function §#
    newLevel = build_level(title, levelMap, theme, levelTime, config, loggedInId)
    db.session.add(newLevel)
    Account.query.filter_by(internalId=loggedInId).first().levelCount += 1
    db.session.commit()

    #§ Grabbing level data from database to send back (Including new levelId) §#
    result = getLevelData(newLevel.internalId)

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": result,
        "updated": getPlayerData(loggedInId,2),
        "timestamp": int(time.time())
        }
    
    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)