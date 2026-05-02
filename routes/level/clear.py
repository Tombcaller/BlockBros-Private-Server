# imports --------------------- #
from flask import Blueprint, request

from models import Interactions, db, Level, Account
from utils.db_item_factory import build_interaction
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_player_data
from utils.decode_batch import decode_batch

import time
from random import randint
from config import clearRewardList


# blueprint, route ------------ #
level_clear_bp = Blueprint("level_clear", __name__, url_prefix="/level")
@level_clear_bp.route("/clear", methods=["POST"])


def clear():
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])

    #§ Grabbing request data and decoding batch §#
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()

    decode_batch(requestData.get("batch"), loggedInId)

    levelId = requestData.get("level_id")
    completionTime = requestData.get("time")
    version = requestData.get("version")           # Useless for now
    video_loaded = requestData.get("video_loaded") # Same as above

    #§ Returning error if any keys are missing from request §#
    if not levelId or not completionTime or not version or not video_loaded:
        return error_response("missing_parameters")

    #-------------------------§#

    levelDifficulty = db.session.query(Level).filter(Level.internalId == levelId).first().difficulty
    firstClear = db.session.query(Interactions).filter_by(levelInternalId=levelId, gamerInternalId=loggedInId).filter(Interactions.completionTime > 0).first() is None

    #§ Adding stats to player after level completion, and recalculate rank §#
    if firstClear:
        Account.query.filter_by(internalId=loggedInId).first().playerPt += levelDifficulty

    PP = Account.query.filter_by(internalId=loggedInId).first().playerPt
    if PP in range(0, 500):
        Account.query.filter_by(internalId=loggedInId).first().rank = 1 #bronze
    if PP in range(500, 2000):
        Account.query.filter_by(internalId=loggedInId).first().rank = 2 #silver
    if PP in range(2000, 10000):
        Account.query.filter_by(internalId=loggedInId).first().rank = 3 #gold
    if PP in range(10000, 80000):
        Account.query.filter_by(internalId=loggedInId).first().rank = 4 #platinum
    if PP in range(80000, 250000):
        Account.query.filter_by(internalId=loggedInId).first().rank = 5 #fire platinum
    if PP in range(250000, 1000000):
        Account.query.filter_by(internalId=loggedInId).first().rank = 6 #cores
    if PP >= 1000000:
        Account.query.filter_by(internalId=loggedInId).first().rank = 7 #love core

    # grabbing already existing interaction for user+level. if not existing, creating new one.
    existingInteraction = db.session.query(Interactions).filter_by(levelInternalId=levelId, gamerInternalId=loggedInId).first()
    if existingInteraction:
        existingInteraction.completionTime = completionTime
    else:
        db.session.add(build_interaction(levelId, loggedInId, completionTime, -1, 0))
    db.session.commit()

    #§ Generating clear reward based on level difficulty §#
    clearRewardItem = clearRewardList[str(levelDifficulty)][randint(1,len(clearRewardList[str(levelDifficulty)]))-1]
    clearReward = {
        "id": clearRewardItem["id"],
        "quantity": clearRewardItem["quantity"],
        "type": clearRewardItem["type"]
    }

    result = {
        "clearReward": clearReward,
        "completed": True,
        "firstClear": firstClear,
        "ownRecord": db.session.query(Interactions).filter_by(levelInternalId=levelId, gamerInternalId=loggedInId).order_by(Interactions.completionTime.asc()).first().completionTime == completionTime,
        "playerPt" : levelDifficulty,
        "rank": db.session.query(Interactions).filter_by(levelInternalId=levelId).order_by(Interactions.completionTime.asc()).all().index(
            db.session.query(Interactions).filter_by(levelInternalId=levelId, gamerInternalId=loggedInId).first()
        ) + 1,
        "time": completionTime,
        "video" : "",
        "videoGem": 0
    }

    body = {
        "success": True,
        "result": result,
        "updated": { "gamer" : get_player_data(loggedInId,2) },
        "timestamp": int(time.time())
    }

    return generate_response(body)  