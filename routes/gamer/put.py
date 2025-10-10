#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

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
gamer_put_bp = Blueprint("gamer_put", __name__, url_prefix="/gamer")
@gamer_put_bp.route("/put", methods=["POST"])

def put():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]: 
        return errorResponse(validity["error"])

    #§ Grabbing current logged in user's internal ID for database usage §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining login params to check in DB from user's request data §#
    nicknameToCheck = request_data.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return errorResponse("missing_parameters")

    #§ Looking up nickname in database §#
    if account.query.filter(func.lower(account.nickname) == nicknameToCheck.lower()).first() is not None:
        success = False
    else:
        #§ Loading data from currently logged in user, updating name version and nickname §#
        currentUser = account.query.filter(account.internalId == loggedInId).first()
        currentUser.nickname = nicknameToCheck
        currentUser.nameVersion += 1
        db.session.commit()
        success = True

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": {},
        "updated": {"gamer": getPlayerData(loggedInId)} if success == True else {},
        "timestamp": 1759854961
        }
    
    #§ Adding missing headers not returned by default §#
    body["updated"]["gamer"]["nameVersion"] = currentUser.nameVersion
    body["updated"]["gamer"]["nameVersion"] = currentUser.gem
    body["updated"]["gamer"]["inventory"] = json.loads(currentUser.inventory)

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)