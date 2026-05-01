#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db, Account, Comment
from utils.response import generateResponse, errorResponse
from utils.db_item_factory import generate_token
from utils.get_db_data import getPlayerData, loadCommentListPage, getCommentData
from config.config import listConfig, mainConfig

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
    accountToLogin = Account.query.filter_by(gamerId=gamerId).first()

    #§ Returning error if gamerId not found in DB §#
    if not accountToLogin:
        return errorResponse("no_match", 200)

    #§ Verifiying that password from request matches that of accountToLogin §#
    if accountToLogin.altPassword != password and mainConfig["adminOverride"]["enabled"] == False:
        return errorResponse("no_match", 200)
    
    elif password != mainConfig["adminOverride"]["password"]:
        return errorResponse("no_match", 200)
    
    #§ Generating new token for user and updating lastLoginAt time §#
    token = generate_token()
    accountToLogin.token = token
    accountToLogin.lastLoginAt = time.time()
    db.session.commit()

    #§ Assigning a group_key for initial feed based on device language §#
    try:
        lang = request.headers.get("Device-Language")
        if lang != "jp":
            group_key = "feed"
        else:
            group_key = "feed_ja"
    except:
        group_key = "feed"

    items, cursorToReturn, allLoaded = loadCommentListPage(Comment.query.filter(Comment.groupKey == group_key).order_by(Comment.createdAt.desc()), "createdAt", "", listConfig["homeFeedItemReturnLimit"])
    jsonCommentList = [getCommentData(c.internalId) for c in items]

    #§ Creating body to send §#
    body = {
        "success": True,
        "result":{
            "loginBonus": 0,
            "token": token,
        },
        "updated":{
            "campaignInfo":{
                "comments":{}
            },
            "feeds":{
                "all_loaded": allLoaded,
                "cursor": cursorToReturn,
                "index": len(items),
                "items": jsonCommentList
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