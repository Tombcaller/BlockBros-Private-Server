#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import account
from utils.response import generateResponse
from utils.account_factory import generate_token

#§ Misc Imports §#
import time
import json
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
        return {"error": "Invalid request"}, 400

    #§ Looking up user in database and saving their data to "accountToLogin" §#
    accountToLogin = account.query.filter_by(gamerId=gamerId).first()

    #§ Returning error if gamerId not found in DB §#
    if not accountToLogin:
        return {"error": "Account not found"}, 404

    #§ Verifiying that password from request matches that of accountToLogin §#
    if accountToLogin.altPassword != password:
        return {"error": "Invalid password"}, 403
    
    #§ Creating body to send §#
    body = {
        "success": True,
        "result":{
            "loginBonus": 0,
            "token": generate_token(),
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
            "gamer":{
                "adminLevel": accountToLogin.adminLevel,
                "altPassword": accountToLogin.altPassword,
                "avatar": accountToLogin.avatar,
                "builderPt": accountToLogin.builderPt,
                "campaigns":{},
                "channel": accountToLogin.channel,
                "clearCount": accountToLogin.clearCount,
                "commentableAt": accountToLogin.commentableAt,
                "country": accountToLogin.country,
                "createdAt": accountToLogin.createdAt,
                "emblemCount": accountToLogin.emblemCount,
                "followerCount": accountToLogin.followerCount,
                "gamerId": accountToLogin.gamerId,
                "gem": accountToLogin.gem,
                "hasUnfinishedIAP": False,
                "homeLevel": accountToLogin.homeLevel,
                "id": accountToLogin.id,
                "inventory": json.loads(accountToLogin.inventory),
                "lang": accountToLogin.lang,
                "lastLoginAt": accountToLogin.lastLoginAt,
                "levelCount": accountToLogin.levelCount,
                "maxVideoId": accountToLogin.maxVideoId,
                "nameVersion": accountToLogin.nameVersion,
                "nickname": accountToLogin.nickname,
                "password": accountToLogin.password,
                "playerPt": accountToLogin.playerPt,
                "researches":[],
                "visibleAt": accountToLogin.visibleAt
            },
            "gifts":[],
            "notifications":[]
        },
        "timestamp": int(time.time())
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)