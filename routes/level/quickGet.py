#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from utils.response import generateResponse, checkToken, tokenMismatchResponse
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
level_quickGet_bp = Blueprint("level_quickGet", __name__, url_prefix="/level")
@level_quickGet_bp.route("/quickGet", methods=["POST"])

def quick_get():

    #§ Checking token validity §#
    if checkToken(request.headers.get("Authorization")) == False:
        return tokenMismatchResponse()

    body = {
        "success": True,
        "result": {
            "all_loaded": True,
            "index": 1,
            "items": [
                {
                    "clearCount": 0,
                    "commentCount": 0,
                    "difficulty": 0,
                    "fav": False,
                    "gamer": {},
                    "title": "temp level for response",
                    "rating": 0,
                    "tier": 0
                }
            ]
        },
        "updated": {},
        "timestamp": 1759665348
    }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)