#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint

#§ Server Utility Imports §#
from utils.response import generateResponse
from config import mainConfig

#§ Misc Imports §#
import time
#§ ------------------------- §#

master_update_bp = Blueprint("master_update", __name__, url_prefix="/master")

@master_update_bp.route("/update", methods=["POST"])
def update():

    respCode = 200

    body = {
            "success": True,
            "result": {},
            "updated": {},
            "timestamp": int(time.time())
            }
    
    if mainConfig["versionLoading"]["enabled"]:
        body["master"] = {
            "config":{
                "assetversion": mainConfig["versionLoading"]["version"]
                }
            }
                
        respCode = 409

    return generateResponse(body, respCode)