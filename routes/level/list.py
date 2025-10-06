from flask import Blueprint, request, Response
import time
import json
import gzip

level_list_bp = Blueprint("level_list", __name__, url_prefix="/level")
@level_list_bp.route("/list", methods=["POST"])

def list():
    return