
#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import db, Level
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getLevelData

#§ Misc Imports §#
import time
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
level_clear_bp = Blueprint("level_clear", __name__, url_prefix="/level")
@level_clear_bp.route("/clear", methods=["POST"])

def clear():
    #§ Checking Request (Token + CRC) validity §#
    validity = checkRequestValidity(request)
    if not validity["success"]:
        return errorResponse(validity["error"])

    db.session.query(Level).delete()
    db.session.commit()

    body = {
        "success": True,
        "result": {},
        "updated": {},
        "timestamp": int(time.time())
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)  