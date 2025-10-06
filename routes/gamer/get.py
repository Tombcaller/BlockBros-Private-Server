from flask import Blueprint, request, Response
import time
import json
import gzip

gamer_get_bp = Blueprint("gamer_get", __name__, url_prefix="/gamer")
@gamer_get_bp.route("/get", methods=["POST"])

def get():
    return