#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getLevelData #tempremental


from utils.db_item_factory import buildLevel #tempremental

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

    #§ Grabbing current logged in user's internal ID for addition to comment §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    title = request_data["title"]
    levelMap = request_data["map"]
    theme = request_data["theme"]
    time = request_data["time"]
    config = request_data["config"]

    if not title or not levelMap or not theme or not time or not config:
        return {"error": "Invalid request"}, 400

    newLevel = buildLevel(title, levelMap, theme, time, config, loggedInId)
    db.session.add(newLevel)
    db.session.commit()

    result = {
        getLevelData(newLevel.internalId)
    }

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": result,
        "updated": {getLevelData(loggedInId, 2)},
        "timestamp": int(time.time())
        }
    
    print("request :"+str(request_data))
    print("response :"+str(body))
    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)