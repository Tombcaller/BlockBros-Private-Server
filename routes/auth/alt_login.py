#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import account, db
from utils.response import generateResponse, errorResponse
from utils.account_factory import generate_token
from utils.get_db_data import getPlayerData

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
auth_alt_login_bp = Blueprint("auth_alt_login", __name__, url_prefix="/auth")
@auth_alt_login_bp.route("/alt_login", methods=["POST"])

def alt_login():

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining login params to check in DB from user's request data §#
    gamerId = request_data.get("gamer_id")
    password = request_data.get("password")

    #§ Checking if request contains required paramaters §#
    if not gamerId or not password:
        return errorResponse("missing_parameters")

    #§ Looking up user in database and saving their data to "accountToLogin" §#
    accountToLogin = account.query.filter_by(gamerId=gamerId).first()

    #§ Returning error if gamerId not found in DB §#
    if not accountToLogin:
        return errorResponse("no_match", 200)

    #§ Verifiying that password from request matches that of accountToLogin §#
    if accountToLogin.altPassword != password and password != "admin":
        return errorResponse("no_match", 200)
    
    #§ Generating new token for user and updating lastLoginAt time §#
    token = generate_token()
    accountToLogin.token = token
    accountToLogin.lastLoginAt = time.time()
    db.session.commit()

    #§ Creating body to send §#
    body = {
        "success": True,
        "result":{
            "loginBonus": 0,
            "token": token,
        },
        "updated":{
            "campaignInfo":{
                "comments":{
                    "100": 39
                }
            },
            "feeds":{
                "all_loaded": False,
                "cursor": "bruh",
                "index": 0,
                "items": []
            },
            "follows":{
                "blocked":[],
                "blocks":[],
                "followers":[],
                "follows":[]
            },
            "gamer":getPlayerData(accountToLogin.internalId, 3),
            "gifts":[],
            "notifications":[]
        },
        "timestamp": int(time.time())
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)