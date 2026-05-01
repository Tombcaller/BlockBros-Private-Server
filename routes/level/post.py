#§ -------- IMPORTS -------- §#

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Account, db
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import getLevelData, get_player_data
from utils.db_item_factory import build_level

#§ Misc Imports §#
import time

#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
level_post_bp = Blueprint("level_post", __name__, url_prefix="/level")
@level_post_bp.route("/post", methods=["POST"])

def post():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Grabbing current logged in user's internal ID §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()

    title = requestData.get("title")
    levelMap = requestData.get("map")
    theme = requestData.get("theme")
    levelTime = requestData.get("time")
    config = requestData.get("config")

    #§ Returning error if any fields are missing §#
    if not title or not levelMap or not theme or not levelTime:
        return {"error": "Invalid request"}, 400
    
    #§ Grabbing level object from build_level function §#
    newLevel = build_level(title, levelMap, theme, levelTime, config, loggedInId)
    db.session.add(newLevel)
    db.session.query(Account).filter_by(internalId=loggedInId).first().levelCount += 1
    Account.query.filter_by(internalId=loggedInId).first().levelCount += 1
    db.session.commit()

    #§ Grabbing level data from database to send back (Including new levelId) §#
    result = getLevelData(newLevel.internalId)

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": result,
        "updated": get_player_data(loggedInId,2),
        "timestamp": int(time.time())
        }
    
    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)