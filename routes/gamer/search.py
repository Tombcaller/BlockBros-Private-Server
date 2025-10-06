from flask import Blueprint, request, Response
import time
import json
import gzip

gamer_search_bp = Blueprint("gamer_search", __name__, url_prefix="/gamer")
@gamer_search_bp.route("/search", methods=["POST"])

def search():
    return
