#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db, Comment
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_comment_data, get_player_data

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
comment_delete_bp = Blueprint("comment_delete", __name__, url_prefix="/comment")
@comment_delete_bp.route("/delete", methods=["POST"])

def delete():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])
    
    #§ Grabbing current logged in user's internal ID for addition to comment §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()
    comment_id = requestData.get("comment_id")

    if not comment_id:
        return error_response("missing_parameters")

    comment_data = get_comment_data(comment_id)

    if comment_data["gamer"]["id"] == int(loggedInId) or get_player_data(loggedInId)["adminLevel"] > 0:
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

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)