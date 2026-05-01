#§ -------- IMPORTS -------- §#
#§ Misc Imports §#
import json
import base64
#§ ------------------------- §#

#§ Function to encode json into a cursor §#
def encode_cursor(payload: dict) -> str:
    raw = json.dumps(payload).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")

#§ Function to decode json from an encoded cursor §#
def decode_cursor(cursorStr: str) -> dict | None:
    if not cursorStr:
        return None
    padding = '=' * (-len(cursorStr) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(cursorStr + padding))
    except Exception:
        return None
    
