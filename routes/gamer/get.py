#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Account
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_player_data

#§ Misc Imports §#
import time
#§ ------------------------- §#

gamer_get_bp = Blueprint("gamer_get", __name__, url_prefix="/gamer")
@gamer_get_bp.route("/get", methods=["POST"])

def get():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()
    decode_batch(requestData.get("batch"))

    gamerIdToCheck = requestData.get("gamer_id")

    #§ Checking if request contains required paramaters §#
    if not gamerIdToCheck:
        return error_response("missing_parameters")
    
    #§ Looking up nickname in database §#
    accountToReturn = Account.query.filter(Account.gamerId == gamerIdToCheck).first()
    if accountToReturn is None:
        success = False
    else:
        success = True

    #§ Creating body to send §#
    body = {
        "success": success,
        "result": get_player_data(accountToReturn.internalId, 2) if success == True else {},
        "updated": {},
        "timestamp": int(time.time())
        }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)