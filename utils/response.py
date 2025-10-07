import json
import gzip
from flask import Response
from models import account

def checkToken(auth):
    id = auth.split(":")[0]
    token = auth.split(":")[1]
    
    user = account.query.filter_by(id=id).first()
    if user and user.token == token:
        return True
    else:
        return False
    
def tokenMismatchResponse():
    body = {
        "reason": "token_mismatch",
    }
    return generateResponse(body, status=400)

#§ GZIPping Flask response for BB client compatability §#
def generateResponse(data: dict, status: int = 200):
    json_str = json.dumps(data, ensure_ascii=False)
    gzipped = gzip.compress(json_str.encode("utf-8"))

    response = Response(gzipped, status=status, mimetype="application/json")
    response.headers["Content-Encoding"] = "gzip"
    return response
