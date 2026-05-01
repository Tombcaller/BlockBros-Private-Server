# imports --------------------- #
from flask import Blueprint, request

from models import db, Level, Account
from utils.db_item_factory import build_completion
from utils.response import generate_response, check_request_validity, error_response
from utils.get_db_data import get_player_data

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

    loggedInId = request.headers.get("Authorization").split(":")[0]

    requestData = request.get_json()
    print('request data:', requestData)

    levelId = requestData.get("levelId")
    completionTime = requestData.get("time")

    #§ NOT YET IMPLEMENTED §#
    version = requestData.get("version")
    video_loaded = requestData.get("video_loaded")
    #§ Kelixe, check discord for plans about this! §#
    batch = requestData.get("batch")

    #§ Returning error if any keys are missing from request §#
    if not levelId or not completionTime or not version or not video_loaded:
        return error_response("missing_parameters")

    Level.query.filter_by(internalId=levelId).first().playCount += batch["level"][str(levelId)]["play"]
    #-------------------------§#

    levelDifficulty = db.session.query(Level).filter(Level.internalId == levelId).first().difficulty

    #§ Adding stats to level + player after level completion §#
    Account.query.filter_by(internalId=loggedInId).first().playerPt += levelDifficulty
    Level.query.filter_by(internalId=levelId).first().clearCount += 1

    #§ Adding completion to db table §#
    db.session.add(build_completion(levelId, loggedInId, completionTime))
    db.session.commit()

    #§ Generating clear reward based on level difficulty §#
    clearRewardItem = clearRewardList[str(levelDifficulty)][randint(1,len(clearRewardList[str(levelDifficulty)]))]
    clearReward = {
        "id": clearRewardItem["id"],
        "quantity": clearRewardItem["quantity"],
        "type": clearRewardItem["type"]
    }

    result = {
        "clearReward": clearReward,
        "completed": True,
        "firstClear": True, # kelixe : always true for now, need to add logic to check if player has cleared before"
        "ownRecord": True, # kelixe : "same"
        "playerPt" : levelDifficulty,
        "rank": 1, # kelixe : "same"
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