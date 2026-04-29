#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getCommentData
from utils.db_item_factory import build_comment

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
comment_post_bp = Blueprint("comment_post", __name__, url_prefix="/comment")
@comment_post_bp.route("/post", methods=["POST"])

def post():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]: 
        return errorResponse(validity["error"])

    #§ Grabbing current logged in user's internal ID for addition to comment §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    commentMessage = request_data["comment"]
    commentGroupKey = request_data["group_key"]

    newComment = build_comment(commentMessage, commentGroupKey, loggedInId)
    db.session.add(newComment)
    db.session.commit()

    result = {
        "comment":getCommentData(newComment.internalId)
    }

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": result,
        "updated": {},
        "timestamp": int(time.time())
        }
    print("request :"+str(request_data))
    print("response :"+str(body))
    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)