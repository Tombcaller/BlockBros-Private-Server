#§ -------- IMPORTS -------- §#
#§ SQLAlchemy Imports §#
from sqlalchemy import func

#§ Flask Imports §#
from flask import Blueprint, request

#§ Server Utility Imports §#
from models import account, db
from utils.response import generateResponse, checkToken, tokenMismatchResponse
#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
gamer_put_bp = Blueprint("gamer_put", __name__, url_prefix="/gamer")
@gamer_put_bp.route("/put", methods=["POST"])

def put():

    #§ Checking token validity §#
    if checkToken(request.headers.get("Authorization")) == False:
        return tokenMismatchResponse()
    else:
        loggedInId = request.headers.get("Authorization").split(":")[0]

    #§ Getting user's request data from Flask §#
    request_data = request.get_json()

    #§ Defining login params to check in DB from user's request data §#
    nicknameToCheck = request_data.get("nickname")

    #§ Checking if request contains required paramaters §#
    if not nicknameToCheck:
        return {"error": "Invalid request"}, 400

    #§ Looking up nickname in database §#
    if account.query.filter(func.lower(account.nickname) == nicknameToCheck.lower()).first() is not None:
        return generateResponse({"success": False, "result": {}, "updated": {}, "timestamp": 1759854937})
    
    currentUser = account.query.filter(account.id == loggedInId).first()
    currentUser.nickname = nicknameToCheck
    db.session.commit()

    #§ Creating body to send §#
    body = {
        "success": True,
        "result": {},
        "updated": {
            "gamer": {
            "adminLevel": currentUser.adminLevel,
            "avatar": 1,
            "builderPt": 0,
            "campaigns": {},
            "channel": "",
            "clearCount": 0,
            "commentableAt": 0,
            "country": "GB",
            "createdAt": 1730916323,
            "emblemCount": 0,
            "followerCount": 0,
            "gamerId": 360684,
            "gem": 85,
            "hasUnfinishedIAP": False,
            "id": 5067488613367808,
            "inventory": {
                "avatars": [
                1
                ],
                "blocks": {
                "3": 2,
                "4": 80,
                "5": 20,
                "6": 20,
                "7": 5,
                "8": 1,
                "9": 3
                },
                "themes": {
                "1": 1
                }
            },
            "lang": "en",
            "lastLoginAt": 1759854921,
            "levelCount": 1,
            "maxVideoId": 0,
            "nameVersion": 2,
            "nickname": "HTTPS",
            "playerPt": 2,
            "researches": None,
            "visibleAt": 0
            }
        },
        "timestamp": 1759854961
        }

    #§ Use utils.response generateResponse to format correctly (GZip + Headers) §#
    return generateResponse(body)