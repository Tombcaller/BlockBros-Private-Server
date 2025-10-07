#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request
from sympy import false

#§ Server Utility Imports §#
from models import account
from utils.response import generateResponse, checkToken, tokenMismatchResponse

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_nickname_check = Blueprint("gamer_nickname_check", __name__, url_prefix="/gamer/nickname")
@gamer_nickname_check.route("/check", methods=["POST"])
def check():

    #§ Checking token validity §#
    if checkToken(request.headers.get("Authorization")) == False:
        return tokenMismatchResponse()

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining params to check in DB from user's request data §#
    nicknameToCheck = request_data.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return {"error": "Invalid request"}, 400
    
    #§ Looking up nickname in database §#
    if account.query.filter(func.lower(account.nickname) == nicknameToCheck.lower()).first() is None:
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

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)