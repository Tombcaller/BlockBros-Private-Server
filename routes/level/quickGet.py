#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db, Level
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getLevelData #tempremental

#§ Misc Imports §#
import time

#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
level_quickGet_bp = Blueprint("level_quickGet", __name__, url_prefix="/level")
@level_quickGet_bp.route("/quickGet", methods=["POST"])


def quickGet():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]:
        return errorResponse(validity["error"])

    randomEntry =  db.session.query(Level).order_by(func.random()).first()
    randomLevel = getLevelData(randomEntry.internalId)

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

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)
