#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import account, db
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getPlayerData

#§ Misc Imports §#
import time
import json
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_channel_set_bp = Blueprint("gamer_channel_set", __name__, url_prefix="/gamer/channel")
@gamer_channel_set_bp.route("/set", methods=["POST"])

def set():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]: 
        return errorResponse(validity["error"])

    #§ Grabbing current logged in user's internal ID for database usage §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining login params to check in DB from user's request data §#
    url = request_data.get("url")

    #§ Checking if request contains required paramaters §#
    if not url:
        return errorResponse("missing_parameters")

    currentUser = account.query.filter(account.internalId == loggedInId).first()
    currentUser.channel = url
    db.session.commit()
    success = True

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": {},
        "updated": {"gamer": getPlayerData(loggedInId)} if success == True else {},
        "timestamp": int(time.time())
        }
    
    body["updated"]["gamer"]["inventory"] = json.loads(currentUser.inventory)

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)