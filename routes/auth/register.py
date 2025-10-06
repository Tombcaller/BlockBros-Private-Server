#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db
from utils.response import generateResponse
from utils.account_factory import build_account

#§ Misc Imports §#
import time
import json
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
auth_register_bp = Blueprint("auth_register", __name__, url_prefix="/auth")
@auth_register_bp.route("/register", methods=["POST"])

def register():

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()

    #§ Defining register params from user's request data §#
    lang = requestData.get("lang")
    key = requestData.get("key")

    #§ Checking if request contains required paramaters §#
    if not lang or not key:
        return {"error": "Invalid request"}, 400

    #§ Checking if key is correct §#
    if key != "Jq983":
        return {"error": "Invalid key"}, 403

    #§ Creating new account with utils.account_factory account builder §#
    newAccount = build_account(lang=lang)

    #§ Adding new account to DB §#
    db.session.add(newAccount)
    db.session.commit()

    #§ Set nickname after ID is assigned §#
    newAccount.nickname = f"{newAccount.gamerId:08d}"
    db.session.commit()

    #§ Creating body to send §#
    body = {
        "success": True,
        "result":{
            "loginBonus": 0,
            "token": newAccount.token,
            "user_id": newAccount.id,
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
                "adminLevel": newAccount.adminLevel,
                "altPassword": newAccount.altPassword,
                "avatar": newAccount.avatar,
                "builderPt": newAccount.builderPt,
                "campaigns":{},
                "channel": newAccount.channel,
                "clearCount": newAccount.clearCount,
                "commentableAt": newAccount.commentableAt,
                "country": newAccount.country,
                "createdAt": newAccount.createdAt,
                "emblemCount": newAccount.emblemCount,
                "followerCount": newAccount.followerCount,
                "gamerId": newAccount.gamerId,
                "gem": newAccount.gem,
                "hasUnfinishedIAP": False,
                "homeLevel": newAccount.homeLevel,
                "id": newAccount.id,
                "inventory": json.loads(newAccount.inventory),
                "lang": "en",
                "lastLoginAt": newAccount.lastLoginAt,
                "levelCount": newAccount.levelCount,
                "maxVideoId": newAccount.maxVideoId,
                "nameVersion": newAccount.nameVersion,
                "nickname": newAccount.nickname,
                "password": newAccount.password,
                "playerPt": newAccount.playerPt,
                "researches":[],
                "visibleAt": newAccount.visibleAt
            },
            "gifts":[],
            "notifications":[]
        },
        "timestamp": int(time.time())
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)