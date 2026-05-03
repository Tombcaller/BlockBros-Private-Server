#§ -------- IMPORTS -------- §#
#§ Server Utility Imports §#
from models import Account, Comment, Level, Interactions
from config import defaultAccount

#§ Misc Imports §#
import json
import time
import random
import string
import re
#§ ------------------------- §#

#§ Functions -- §#
def generate_password():
    hexChars = '0123456789abcdef'
    hexString = ''.join(random.choice(hexChars) for _ in range(40))
    randomString = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(11))
    return f"{hexString}$sha1${randomString}"

def generate_altPassword():
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=8))

def generate_token():
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=30))

def generate_internalId():
    return random.randint(4000000000000000, 7000000000000000)

def get_comment_type(commentMessage, loggedInId):
    #§ Define regex patterns for each category #§
    levelPattern      = r"#[0-9]+"
    tagPattern        = r"#[A-Za-z_]\w*"
    kamVideoIdPattern = r"%[0-9]+"
    emblemPattern     = r"\$[0-9]+"
    youtubePattern    = r":youtube"
    reviewPattern     = r"#star"

    #§ Combined pattern to find the first occurrence of any of them §#
    combinedPattern = rf"(?:{levelPattern}|{tagPattern}|{emblemPattern}|{kamVideoIdPattern}|{youtubePattern}|{reviewPattern})"

    match = re.search(combinedPattern, commentMessage)

    result = None

    if match:
        token = match.group(0)

        if re.fullmatch(youtubePattern, token):
            channel = Account.query.filter(Account.internalId == loggedInId).first().channel
            if channel != "":
                result = {"args": {"youtube": channel}, "type": "youtube", "message": commentMessage.strip(token)}
            else:
                result = {"args": {}, "type": "plain", "message": commentMessage.strip(token)}
        
        elif re.fullmatch(emblemPattern, token):
            result = {"args": {"refId": token[1:]}, "type": "emblem", "message": commentMessage.strip(token)}

        elif re.fullmatch(kamVideoIdPattern, token):
            result = {"args": {"kamVideoId": token[1:]}, "type": "video", "message": commentMessage.strip(token)}

        elif re.fullmatch(tagPattern, token) and token[1:] != "star":
            result = {"args": {"tag": token[1:]}, "type": "tag", "message": commentMessage.strip(token)}

        elif re.fullmatch(levelPattern, token):
            result = {"args": {"levelId": int(token[1:]) + 10000}, "type": "level", "message": commentMessage.strip(token)}

        elif re.fullmatch(reviewPattern, token):
            result = {"args": {}, "type": "review", "message": commentMessage.strip(token)}

    else:
        result = {"args": {}, "type": "plain", "message": commentMessage}

    return(result)
#§--------------§#

#§ Account builder function with default language being "en". §#
def build_account(lang="en"):

    data = defaultAccount
    
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

    #§ Returning new Account object §#
    return Account(**data)

def build_comment(message = "", groupKey = "feed", gamerInternalId = 0):
    typeData = get_comment_type(message, gamerInternalId)
    data = {
        "messageType": typeData["type"],
        "groupKey": groupKey,
        "internalId": generate_internalId(),
        "args": typeData["args"],
        "createdAt": time.time(),
        "gamerInternalId": gamerInternalId,
        "message": typeData["message"]
    }
    return Comment(**data)


def build_level(title = "", levelMap = "", theme = "", levelTime = "", config = "", gamerInternalId = 0):
    data = {
        "title": title,
        "levelMap": levelMap,
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

def build_interaction(levelInternalId, gamerInternalId, completionTime, givenRating, fav):
    data = {
        "internalId": generate_internalId(),
        "levelInternalId": levelInternalId,
        "gamerInternalId": gamerInternalId,
        "completionTime": completionTime,
        "givenRating": givenRating,
        "fav": fav
    }
    return Interactions(**data)
