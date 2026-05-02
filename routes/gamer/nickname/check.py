#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Account
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_nickname_check_bp = Blueprint("gamer_nickname_check", __name__, url_prefix="/gamer/nickname")
@gamer_nickname_check_bp.route("/check", methods=["POST"])

def check():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()
    decode_batch(request_data.get("batch"))

    #§ Defining params to check in DB from user's request data §#
    nicknameToCheck = request_data.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return error_response()
    
    #§ Looking up nickname in database §#
    if Account.query.filter(func.lower(Account.nickname) == nicknameToCheck.lower()).first() is None:
        success = True
    else:
        success = False

    #§ Creating body to send §#
    body = {
        "success": success,
        "result":{},
        "updated":{},
        "timestamp": int(time.time())
    }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)