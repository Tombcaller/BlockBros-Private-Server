#§ -------- IMPORTS -------- §#
#§ Misc Imports §#
import json
import base64
#§ ------------------------- §#

def encode_cursor(payload: dict) -> str:
    raw = json.dumps(payload).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")

def decode_cursor(cursor_str: str) -> dict | None:
    if not cursor_str:
        return None
    padding = '=' * (-len(cursor_str) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(cursor_str + padding))
    except Exception:
        return None
    
