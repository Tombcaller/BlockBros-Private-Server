#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Blueprint, request

from utils import decode_batch
from utils.response import check_request_validity, error_response

#§ Server Utility Imports §#


#§ Misc Imports §#

#§ ------------------------- §#

#§ Creating endpoint blueprint & setting route §#
emblem_gift_bp = Blueprint("emblem_gift", __name__, url_prefix="/emblem")
@emblem_gift_bp.route("/gift", methods=["POST"])

def gift():

    #§ validity check§#
    validity = check_request_validity(request)
    if not validity["success"]:
        return error_response(validity["error"])
    
    #§ request data and batch processing §#
    loggedInId = request.headers.get("Authorization").split(":")[0]
    requestData = request.get_json()
    decode_batch(requestData.get("batch"), loggedInId)

    #§ grabbing data if valid §#
    emblemId = requestData.get("emblem_id")
    targetGamerId = requestData.get("target_gamer_id")
    
    if not emblemId or not targetGamerId:
        return error_response("missing_parameters")
    