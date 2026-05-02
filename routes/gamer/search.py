#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

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

gamer_search_bp = Blueprint("gamer_search", __name__, url_prefix="/gamer")
@gamer_search_bp.route("/search", methods=["POST"])

def search():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    #§ Defining params to check in DB from user's request data §#
    nicknameToCheck = requestData.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return error_response("missing_parameters")
    
    #§ Looking up nickname in database §#
    accountToReturn = Account.query.filter(func.lower(Account.nickname) == nicknameToCheck.lower()).first()
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
            "items": [get_player_data(accountToReturn.internalId)] if success else [],
        },
        "updated": {},
        "timestamp": int(time.time())
        }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)