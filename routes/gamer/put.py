#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import account, db
from utils.response import generateResponse, checkToken, tokenMismatchResponse
from utils.get_db_data import getPublicPlayerData
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_put_bp = Blueprint("gamer_put", __name__, url_prefix="/gamer")
@gamer_put_bp.route("/put", methods=["POST"])

def put():

    #§ Checking token validity §#
    if checkToken(request.headers.get("Authorization")) == False:
        return tokenMismatchResponse()
    else:
        loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining login params to check in DB from user's request data §#
    nicknameToCheck = request_data.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return {"error": "Invalid request"}, 400

    #§ Looking up nickname in database §#
    if account.query.filter(func.lower(account.nickname) == nicknameToCheck.lower()).first() is not None:
        print("Invalid.")
        return generateResponse({"success": False, "result": {}, "updated": {}, "timestamp": 1759854937})
    
    print("Invalid 2")
    currentUser = account.query.filter(account.internalId == loggedInId).first()
    currentUser.nickname = nicknameToCheck
    currentUser.nameVersion += 1
    db.session.commit()

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": {},
        "updated": {
            "gamer": getPublicPlayerData(loggedInId)
        },
        "timestamp": 1759854961
        }
    
    body["updated"]["gamer"]["nameVersion"] = currentUser.nameVersion

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)