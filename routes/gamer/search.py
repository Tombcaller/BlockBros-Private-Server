#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import account
from utils.response import generateResponse, checkToken, tokenMismatchResponse
from utils.get_db_data import getPlayerData

#§ Misc Imports §#
import time
#§ ------------------------- §#

gamer_search_bp = Blueprint("gamer_search", __name__, url_prefix="/gamer")
@gamer_search_bp.route("/search", methods=["POST"])

def search():
    #§ Checking token validity §#
    if checkToken(request.headers.get("Authorization")) == False:
        return tokenMismatchResponse()
    else:
        loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining params to check in DB from user's request data §#
    nicknameToCheck = request_data.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return {"error": "Invalid request"}, 400
    
    #§ Looking up nickname in database §#
    accountToReturn = account.query.filter(func.lower(account.nickname) == nicknameToCheck.lower()).first()
    if accountToReturn is None:
        success = False
    else:
        success = True

    #§ Creating body to send §#
    body = {
        "success": success,
        "result": {
            "all_loaded": True,
            "index": 1 if success else 0,
            "items": [getPlayerData(accountToReturn.internalId)] if success == True else [],
        },
        "updated": {},
        "timestamp": int(time.time())
        }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)