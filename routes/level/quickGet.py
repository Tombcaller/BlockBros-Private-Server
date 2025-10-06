#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint

#§ Server Utility Imports §#
from utils.response import generateResponse
from models import db
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
level_quickGet_bp = Blueprint("level_quickGet", __name__, url_prefix="/level")
@level_quickGet_bp.route("/quickGet", methods=["POST"])

def quick_get():
    body = {
        "success": True,
        "result": {
            "all_loaded": True,
            "index": 1,
            "items": [
                {
                    "clearCount": 38,
                    "commentCount": 1,
                    "difficulty": 2,
                    "fav": False,
                    "gamer": {
                        "gamerId": 63125,
                        "nickname": "ANNIN豆腐",
                        "country": "JP",
                    },
                    "title": "噛まれるな！",
                    "rating": 42,
                    "tier": 1
                }
            ]
        },
        "updated": {},
        "timestamp": 1759665348
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)