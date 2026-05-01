#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

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
gamer_put_bp = Blueprint("gamer_put", __name__, url_prefix="/gamer")
@gamer_put_bp.route("/put", methods=["POST"])

def put():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Grabbing current logged in user's internal ID for database usage §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining login params to check in DB from user's request data §#
    nicknameToCheck = request_data.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return error_response("missing_parameters")

    #§ Looking up nickname in database §#
    if Account.query.filter(func.lower(Account.nickname) == nicknameToCheck.lower()).first() is not None:
        success = False
    else:
        #§ Loading data from currently logged in user, updating name version and nickname §#
        currentUser = Account.query.filter(Account.internalId == loggedInId).first()
        currentUser.nickname = nicknameToCheck
        currentUser.nameVersion += 1
        db.session.commit()
        success = True

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": {},
        "updated": {"gamer": get_player_data(loggedInId)} if success == True else {},
        "timestamp": int(time.time())
        }
    
    #§ Adding missing headers not returned by default §#
    body["updated"]["gamer"]["nameVersion"] = currentUser.nameVersion
    body["updated"]["gamer"]["gem"] = currentUser.gem
    body["updated"]["gamer"]["inventory"] = json.loads(currentUser.inventory)

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)