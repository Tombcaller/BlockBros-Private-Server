#§ -------- IMPORTS -------- §#
#§ Server Utility Imports §#
from pathlib import Path
from models import account, comment, Level

#§ Misc Imports §#
import json
import time
import random
import string
import re
#§ ------------------------- §#

#§ Functions -- §#
def generate_password():
    hex_chars = '0123456789abcdef'
    hex_string = ''.join(random.choice(hex_chars) for _ in range(40))
    random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(11))
    return f"{hex_string}$sha1${random_string}"

def generate_altPassword():
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=8))

def generate_token():
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=30))

def generate_internalId():
    return random.randint(4000000000000000, 7000000000000000)

def get_comment_type(comment_message, loggedInId):
    #§ Define regex patterns for each category #§
    level_pattern      = r"#[0-9]+"
    tag_pattern        = r"#[A-Za-z_]\w*"
    kamVideoId_pattern = r"%[0-9]+"
    emblem_pattern     = r"\$[0-9]+"
    youtube_pattern    = r":youtube"
    review_pattern     = r"#star"

    #§ Combined pattern to find the first occurrence of any of them §#
    combined_pattern = rf"(?:{level_pattern}|{tag_pattern}|{emblem_pattern}|{kamVideoId_pattern}|{youtube_pattern}|{review_pattern})"

    match = re.search(combined_pattern, comment_message)

    result = None

    if match:
        token = match.group(0)

        if re.fullmatch(youtube_pattern, token):
            channel = account.query.filter(account.internalId == loggedInId).first().channel
            if channel != "":
                result = {"args": {"youtube": channel}, "type": "youtube", "message": comment_message.strip(token)}
            else:
                result = {"args": {}, "type": "plain", "message": comment_message.strip(token)}
        
        elif re.fullmatch(emblem_pattern, token):
            result = {"args": {"refId": token[1:]}, "type": "emblem", "message": comment_message.strip(token)}

        elif re.fullmatch(kamVideoId_pattern, token):
            result = {"args": {"kamVideoId": token[1:]}, "type": "video", "message": comment_message.strip(token)}

        elif re.fullmatch(tag_pattern, token) and token[1:] != "star":
            result = {"args": {"tag": token[1:]}, "type": "tag", "message": comment_message.strip(token)}

        elif re.fullmatch(level_pattern, token):
            result = {"args": {"levelId": token[1:]}, "type": "level", "message": comment_message.strip(token)}

        elif re.fullmatch(review_pattern, token):
            result = {"args": {}, "type": "review", "message": comment_message.strip(token)}

    else:
        result = {"args": {}, "type": "plain", "message": comment_message}

    return(result)
#§--------------§#

#§ Account builder function with default language being "en". §#
def build_account(lang="en"):

    #§ Loading default account template from JSON config file §#
    defaults_path = Path(__file__).resolve().parents[1] / "config" / "defaults" / "default_account.json"
    with open(defaults_path, "r", encoding="utf-8") as f:
        default_data = json.load(f)

    #§ Initially copying data from json file §#
    data = default_data.copy()
    
    #§ Updating data with generated values §#
    data.update({
        "nickname": None,
        "password": generate_password(),
        "altPassword": generate_altPassword(),
        "createdAt": time.time(),
        "lastLoginAt": time.time(),
        "internalId": generate_internalId(),
        "token": generate_token(),
        "lang": lang
    })

    #§ Returning new account object §#
    return account(**data)

def build_comment(message = "", groupKey = "feed", gamerInternalId = 0):
    typeData = get_comment_type(message, gamerInternalId)
    data = {
        "messageType": typeData["type"],
        "groupKey": groupKey,
        "internalId": generate_internalId(),
        "args": json.dumps(typeData["args"]),
        "createdAt": time.time(),
        "gamerInternalId": gamerInternalId,
        "message": typeData["message"]
    }
    return comment(**data)


def build_level(title = "", levelMap = "", theme = "", levelTime = "", config = "", gamerInternalId = 0):
    data = {
        "title": title,
        "map": levelMap,
        "theme": theme,
        "time": levelTime,
        "config": config,
        "internalId": generate_internalId(),
        "createdAt": time.time(),
        "gamerInternalId": gamerInternalId,

        "clearCount": 1,
        "clearVersion": 1,
        "commentCount": 0,
        "commentedAt": 0,
        "difficulty": 1,
        "draft": 0,
        "playCount": 0,
        "rating": 0,
        "ratingCount": 0,
        "tag": "",
        "tier": 0,
        "todayRating": 0,
        "uuClearCount": 0,
        "uuCount": 0,
        "version": 1,
        "yesterdayRating": 0
        
    }
    return Level(**data)
