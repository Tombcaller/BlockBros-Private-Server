#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint

#§ Server Utility Imports §#
from utils.response import generateResponse

#§ Misc Imports §#
import time
import json
from pathlib import Path
#§ ------------------------- §#

master_update_bp = Blueprint("master_update", __name__, url_prefix="/master")

config_path = Path(__file__).resolve().parents[2] / "config" / "config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

@master_update_bp.route("/update", methods=["POST"])
def update():

    respCode = 200

    body = {
            "success": True,
            "result": {},
            "updated": {},
            "timestamp": int(time.time())
            }
    
    if config["versionLoading"]["enabled"]:
        body["master"] = {
            "config":{
                "assetversion": config["versionLoading"]["version"]
                }
            }
                
        respCode = 409

    return generateResponse(body, respCode)