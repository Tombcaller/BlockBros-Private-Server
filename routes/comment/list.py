#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import Comment
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_comment_data, load_comment_list_page
from config import listConfig

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
comment_list_bp = Blueprint("comment_list", __name__, url_prefix="/comment")
@comment_list_bp.route("/list", methods=["POST"])

def list():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()
    group_key = request_data.get("group_key")
    index = int(request_data.get("index", 0))
    cursor = request_data.get("cursor")

    if not group_key:
        return error_response("missing_parameters")
    
    cursor_field = "createdAt"
    query = Comment.query.filter(Comment.groupKey == group_key).order_by(Comment.createdAt.desc())
    
    items, cursorToReturn, allLoaded = load_comment_list_page(query, cursor_field, cursor, listConfig["itemReturnLimit"])
    jsonCommentList = [get_comment_data(c.internalId) for c in items]

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

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)