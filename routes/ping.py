from flask import Blueprint
import time

from models import db, PingLog

ping_bp = Blueprint("ping", __name__, url_prefix="/ping")

@ping_bp.route("/", methods=["GET"])
def ping():
    log = PingLog(timestamp=time.time())  # create row
    db.session.add(log)                   # stage it
    db.session.commit()                   # save to DB
    return {"response": "pong", "timestamp": log.timestamp}