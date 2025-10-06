import json
import gzip
from flask import Response

#§ GZIPping Flask response for BB client compatability §#
def generateResponse(data: dict, status: int = 200):
    json_str = json.dumps(data, ensure_ascii=False)
    gzipped = gzip.compress(json_str.encode("utf-8"))

    response = Response(gzipped, status=status, mimetype="application/json")
    response.headers["Content-Encoding"] = "gzip"
    return response
