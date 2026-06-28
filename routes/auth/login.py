#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Account, db, Comment
from utils.decode_batch import decode_batch
from utils.response import generate_response, error_response
from utils.db_item_factory import generate_token
from utils.get_db_data import get_player_data, load_comment_list_page, get_comment_data
from config import listConfig

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
auth_login_bp = Blueprint("auth_login", __name__, url_prefix="/auth")
@auth_login_bp.route("/login", methods=["POST"])

def login():
    #§ Getting user's request data from Flask §#
    requestData = request.get_json()
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Defining login params to check in DB from user's request data §#
    internalId = requestData.get("id")
    password = requestData.get("password")

    decode_batch(requestData.get("batch"), loggedInId)

    #§ Checking if request contains required paramaters §#
    if not internalId or not password:
        return error_response("missing_parameters")

    #§ Looking up user in database and saving their data to "accountToLogin" §#
    accountToLogin = Account.query.filter_by(internalId=internalId).first()

    #§ Returning error if gamerId not found in DB §#
    if not accountToLogin:
        return error_response("account_not_found")

    #§ Verifiying that password from request matches that of accountToLogin §#
    if accountToLogin.password != password:
        print(accountToLogin.password + " " + password)
        return error_response("no_match")
    
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

    cursor_field = "createdAt"
    items, cursorToReturn, allLoaded = load_comment_list_page(Comment.query.filter(Comment.groupKey == group_key).order_by(Comment.createdAt.desc()), cursor_field, "", listConfig["itemReturnLimit"])
    jsonCommentList = [get_comment_data(c.internalId) for c in items]


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
            "gamer": get_player_data(internalId, 3),
            "gifts":[],
            "notifications":[]
        },
        "timestamp": int(time.time())
    }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)