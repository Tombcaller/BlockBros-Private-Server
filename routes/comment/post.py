#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_comment_data
from utils.db_item_factory import build_comment

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
comment_post_bp = Blueprint("comment_post", __name__, url_prefix="/comment")
@comment_post_bp.route("/post", methods=["POST"])

def post():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]: 
        return error_response(validity["error"])

    #§ Grabbing current logged in user's internal ID for addition to comment §# 
    loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    requestData = request.get_json()

    commentMessage = requestData.get("comment")
    commentGroupKey = requestData.get("group_key")

    if not commentMessage or not commentGroupKey:
        return error_response("missing_parameters")

    newComment = build_comment(commentMessage, commentGroupKey, loggedInId)
    db.session.add(newComment)
    db.session.commit()

    result = {
        "comment":get_comment_data(newComment.internalId)
    }

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": result,
        "updated": {},
        "timestamp": int(time.time())
        }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)