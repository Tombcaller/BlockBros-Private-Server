#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import comment, db
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getCommentData, loadCommentListPage
from config.listConfig import itemReturnLimit

#§ Misc Imports §#
import time
import json
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
comment_list_bp = Blueprint("comment_list", __name__, url_prefix="/comment")
@comment_list_bp.route("/list", methods=["POST"])

def list():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]: 
        return errorResponse(validity["error"])

    #§ Grabbing current logged in user's internal ID for database usage §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()
    group_key = request_data.get("group_key")
    index = int(request_data.get("index", 0))
    cursor = request_data.get("cursor")

    if not group_key:
        return errorResponse("missing_parameters")
    
    cursor_field = "createdAt"
    query = comment.query.order_by(comment.createdAt.desc())
    
    items, cursorToReturn, allLoaded = loadCommentListPage(query, cursor_field, cursor, itemReturnLimit)
    jsonCommentList = [getCommentData(c.internalId) for c in items]

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": {
            "all_loaded": allLoaded,
            "cursor": cursorToReturn,
            "index": index + len(items),
            "items": jsonCommentList
        },
        "updated": {},
        "timestamp": int(time.time())
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)