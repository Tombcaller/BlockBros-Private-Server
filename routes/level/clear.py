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

    #§-------------------------§#

    level = db.session.query(Level).filter(Level.internalId == levelId).first()
    if not level:
        return error_response("invalid_level_id")

    levelDifficulty = level.difficulty
    levelOwnerId = level.gamerInternalId
    
    interaction = db.session.query(Interactions).filter_by(levelInternalId=levelId, gamerInternalId=loggedInId).first()
    
    #§ Checking if player has already completed level §#
    firstClear = db.session.query(Interactions)\
        .filter_by(levelInternalId=levelId, gamerInternalId=loggedInId)\
        .filter(Interactions.completionTime > 0).first() is None
    
    account = Account.query.filter_by(internalId=loggedInId).first()

    #§ Adding stats to player after level completion, and recalculate rank §#
    if firstClear: account.playerPt += levelDifficulty

    # grabbing already existing interaction for user+level. if not existing, creating new one.
    if interaction: interaction.completionTime = completionTime

    # will rarely trigger; batch should create interaction normally
    else: db.session.add(build_interaction(levelId, loggedInId, completionTime, -1, 0))

    db.session.commit()

    #§ Checking if player has completed level already or owns the level §#
    if firstClear and loggedInId != levelOwnerId:

        #§ Generating clear reward based on level difficulty §#
        clearRewardItem = clearRewardList[str(levelDifficulty)][randint(1,len(clearRewardList[str(levelDifficulty)]))-1]
        clearReward = {
            "id": clearRewardItem["id"],
            "quantity": clearRewardItem["quantity"],
            "type": clearRewardItem["type"]
        }

        playerPtReward = levelDifficulty

    #§ Returning no rewards if level completed previously or owned by logged in player §#
    else:
        clearReward = {}
        playerPtReward = 0    

    #§ Building result §#
    result = {
        "clearReward": clearReward,
        "completed": True,
        "firstClear": firstClear,
        "ownRecord": db.session.query(Interactions).filter_by(levelInternalId=levelId, gamerInternalId=loggedInId).order_by(Interactions.completionTime.asc()).first().completionTime == completionTime and firstClear == False,
        "playerPt" : playerPtReward,
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