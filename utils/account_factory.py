#§ -------- IMPORTS -------- §#
#§ Server Utility Imports §#
from pathlib import Path
from models import account

#§ Misc Imports §#
import json
import time
import random
import string
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
#§--------------§#

#§ Loading default account template from JSON config file §#
defaults_path = Path(__file__).resolve().parents[1] / "config" / "defaults" / "default_account.json"
with open(defaults_path, "r", encoding="utf-8") as f:
    default_data = json.load(f)

#§ Account builder function with default language being "en". §#
def build_account(lang="en"):

    #§ Initially copying data from json file §#
    data = default_data.copy()
    
    #§ Updating data with generated values §#
    data.update({
        "nickname": None,
        "password": generate_password(),
        "altPassword": generate_altPassword(),
        "createdAt": time.time(),
        "lastLoginAt": time.time(),
        "internalId": random.randint(4000000000000000, 7000000000000000),
        "token": generate_token(),
        "lang": lang
    })

    #§ Returning new account object §#
    return account(**data)
