#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Response

#§ Server Utility Imports §#
from models import account

#§ Misc Imports §#
import json
import gzip
#§ ------------------------- §#

#§ Function to check if Authorization header is valid §#
def checkToken(auth):

    #§ Extracting id and token from Authorization header §#
    id = auth.split(":")[0]
    token = auth.split(":")[1]

    #§ Querying DB to see if token from the auth header matches that of the ID from the header §#
    user = account.query.filter_by(id=id).first()

    if user and user.token == token:
        return True
    else:
        return False













#§ Function to generate a response for token mismatch errors §#
def tokenMismatchResponse():   
    body = {
        "reason": "token_mismatch",
    }
    #§ Generating token mismatch response with a 400 error §#
    return generateResponse(body, status=400)

#§ Function to GZIP Flask response for BB client compatability §#
def generateResponse(data: dict, status: int = 200):

    #§ GZIPping response data §#
    json_str = json.dumps(data, ensure_ascii=False)
    gzipped = gzip.compress(json_str.encode("utf-8"))

    #§ Creating & returning Flask Response with GZIPped data and content encoding header §#
    response = Response(gzipped, status=status, mimetype="application/json")
    response.headers["Content-Encoding"] = "gzip"

    return response
