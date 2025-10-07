from flask import Blueprint
import time

master_update_bp = Blueprint("master_update", __name__, url_prefix="/master")

@master_update_bp.route("/update", methods=["POST"])
def register():
    return {
            "success": True,
            "result": {},
            "updated": {},
            "timestamp": int(time.time())
            }