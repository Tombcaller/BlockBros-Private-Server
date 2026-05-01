#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db, Comment
from utils.response import generate_response, error_response
from utils.db_item_factory import build_account
from utils.get_db_data import get_player_data, load_comment_list_page, get_comment_data
from config import listConfig

#§ Misc Imports §#
import time
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
        return error_response("missing_parameters")

    #§ Checking if key is correct §#
    if key != "Jq983":
        return error_response("invalid_key")
        
    #§ Creating new Account with utils.account_factory Account builder §#
    newAccount = build_account(lang=lang)

    #§ Adding new Account to DB §#
    db.session.add(newAccount)
    db.session.commit()

    #§ Set nickname after ID is assigned §#
    newAccount.nickname = f"{newAccount.gamerId:08d}"
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
    items, cursorToReturn, allLoaded = load_comment_list_page(Comment.query.filter(Comment.groupKey == group_key).order_by(Comment.createdAt.desc()), cursor_field, "", listConfig["homeFeedItemReturnLimit"])
    jsonCommentList = [get_comment_data(c.internalId) for c in items]

    #§ Creating body to send §#
    body = {
        "success": True,
        "result":{
            "loginBonus": 0,
            "token": newAccount.token,
            "user_id": newAccount.internalId,
        },
        "updated":{
            "campaignInfo":{
                "comments":{
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
            "gamer": get_player_data(newAccount.internalId, 3),
            "gifts":[],
            "notifications":[]
        },
        "timestamp": int(time.time())
    }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)