#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db, Level
from utils.decode_batch import decode_batch
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_level_data

#§ Misc Imports §#
import time

#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
level_quickGet_bp = Blueprint("level_quickGet", __name__, url_prefix="/level")
@level_quickGet_bp.route("/quickGet", methods=["POST"])


def quickGet():
    #§ Checking Request (Token + CRC) validity §#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    
    loggedInId = request.headers.get("Authorization").split(":")[0]
    
    #§ Getting user's request data from Flask §#
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    randomEntry = db.session.query(Level).order_by(func.random()).first()

    randomLevel = get_level_data(randomEntry.internalId)

    body = {
        "success": True,
        "result": {
            "all_loaded": True,
            "index": 1,
            "items": [
                randomLevel
            ]
        },
        "updated": {},
        "timestamp": int(time.time())
    }

    #§ Use utils.response generate_response to format correctly (GZip + Headers) §#
    return generate_response(body)
