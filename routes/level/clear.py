# imports --------------------- #
from flask import Blueprint, request

from models import db, Level, Account
from utils.db_item_factory import build_completion
from utils.response import generateResponse, checkRequestValidity, errorResponse
from utils.get_db_data import getLevelData, getPlayerData

import time
from random import randint
from config.submaster import clearRewardList



# blueprint, route ------------ #
level_clear_bp = Blueprint("level_clear", __name__, url_prefix="/level")
@level_clear_bp.route("/clear", methods=["POST"])



def clear():
    validity = checkRequestValidity(request)
    if not validity["success"]:
        return errorResponse(validity["error"])

    loggedInId = request.headers.get("Authorization").split(":")[0]


    request_data = request.get_json()
    print('request data:', request_data)
    level_id = request_data.get("level_id")
    completionTime = request_data.get("time")
    version = request_data.get("version")
    video_loaded = request_data.get("video_loaded")
    batch = request_data.get("batch")
    levelDifficulty = db.session.query(Level).filter(Level.internalId == level_id).first().difficulty


    Account.query.filter_by(internalId=loggedInId).first().playerPt += 1
    Level.query.filter_by(internalId=level_id).first().clearCount += 1
    Level.query.filter_by(internalId=level_id).first().playCount += batch["level"][str(level_id)]["play"]
    db.session.add(build_completion(level_id, loggedInId, completionTime))
    db.session.commit()


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
        "updated": { "gamer" : getPlayerData(loggedInId,2) },
        "timestamp": int(time.time())
    }

    return generateResponse(body)  