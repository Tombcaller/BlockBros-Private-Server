#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import account
from utils.response import generateResponse, checkRequestValidity
from utils.get_db_data import getPlayerData

#§ Misc Imports §#
import time
#§ ------------------------- §#

gamer_get_bp = Blueprint("gamer_get", __name__, url_prefix="/gamer")
@gamer_get_bp.route("/get", methods=["POST"])

def get():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]: return validity["error"]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining params to check in DB from user's request data §#
    gamerIdToCheck = request_data.get("gamer_id")

    #§ Checking if request contains required paramaters §#
    if not gamerIdToCheck:
        return {"error": "Invalid request"}, 400
    
    #§ Looking up nickname in database §#
    accountToReturn = account.query.filter(account.gamerId == gamerIdToCheck).first()
    if accountToReturn is None:
        success = False
    else:
        success = True

    #§ Creating body to send §#
    body = {
        "success": success,
        "result": getPlayerData(accountToReturn.internalId, 2) if success == True else {},
        "updated": {},
        "timestamp": int(time.time())
        }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)