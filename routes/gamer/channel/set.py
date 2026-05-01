#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Account, db
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_player_data

#§ Misc Imports §#
import time
import json
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_channel_set_bp = Blueprint("gamer_channel_set", __name__, url_prefix="/gamer/channel")
@gamer_channel_set_bp.route("/set", methods=["POST"])

def set():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Grabbing current logged in user's internal ID for database usage §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()

    #§ Defining login params to check in DB from user's request data §#
    url = requestData.get("url")

    #§ Checking if request contains required paramaters §#
    if not url:
        return error_response("missing_parameters")

    currentUser = Account.query.filter(Account.internalId == loggedInId).first()
    currentUser.channel = url
    db.session.commit()
    success = True

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": {},
        "updated": {"gamer": get_player_data(loggedInId)} if success == True else {},
        "timestamp": int(time.time())
        }
    
    body["updated"]["gamer"]["inventory"] = json.loads(currentUser.inventory)

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)