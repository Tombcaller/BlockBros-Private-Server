#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db, Comment
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getCommentData, getPlayerData

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
comment_delete_bp = Blueprint("comment_delete", __name__, url_prefix="/comment")
@comment_delete_bp.route("/delete", methods=["POST"])

def delete():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]: 
        return errorResponse(validity["error"])
    
    #§ Grabbing current logged in user's internal ID for addition to comment §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()
    comment_id = request_data.get("comment_id")

    if not comment_id:
        return errorResponse("missing_parameters")

    comment_data = getCommentData(comment_id)

    if comment_data["gamer"]["id"] == int(loggedInId) or getPlayerData(loggedInId)["adminLevel"] > 0:
        commentData = Comment.query.get(comment_id)
        db.session.delete(commentData)
        db.session.commit()
        result = {"commentId": comment_id}
    else: result = {}

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": result,
        "updated": {},
        "timestamp": int(time.time())
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)