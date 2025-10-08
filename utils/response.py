#§ -------- IMPORTS -------- §#
#§ Flask Imports §#
from flask import Response

#§ Server Utility Imports §#
from models import account

#§ Misc Imports §#
import json
import gzip
import hashlib
#§ ------------------------- §#

#§ Function to check if are valid §#
def checkRequestValidity(request):

    #§ Extracting id and token from Authorization header §#
    internalId = request.headers.get("Authorization").split(":")[0]
    token = request.headers.get("Authorization").split(":")[1]

    #§ Querying DB to see if token from the auth header matches that of the id from the header §#
    user = account.query.filter_by(internalId=internalId).first()

    #§ Checking for valid token §#
    if user and user.token == token:

        #§ If token is correct, check CRC §#
        body = request.get_json()
        body = json.dumps(body, sort_keys=True, separators=(',', ':'))
        expectedCRC = hashlib.md5(str(body + token).encode("utf-8")).hexdigest()

        if expectedCRC == request.headers.get("CRC"):
            return {"success":True, "error": None}
        else:
            return {"success":False, "error":crcMismatchResponse()}
    else:
        return {"success":False, "error":tokenMismatchResponse()}
    

def crcMismatchResponse():
    body = {
        "reason": "crc_mismatch",
    }
    #§ Generating token mismatch response with a 400 error §#
    return generateResponse(body, status=400)


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
