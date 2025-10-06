from flask import Blueprint, request, Response
import time
import json
import gzip

level_get_bp = Blueprint("level_get", __name__, url_prefix="/level")
@level_get_bp.route("/get", methods=["POST"])

def get():
    return