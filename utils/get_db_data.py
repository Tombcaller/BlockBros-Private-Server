#§ -------- IMPORTS -------- §#
#§ Server Utility Imports §#
from models import account

#§ Misc Imports §#
import json
#§ ------------------------- §#

def getPlayerData(internalId, level = 1):
    accountData = account.query.filter_by(internalId=internalId).first()

    accountToReturn = {
        "adminLevel": accountData.adminLevel,
        "avatar": accountData.avatar,
        "builderPt": accountData.builderPt,
        "channel": accountData.channel,
        "commentableAt": accountData.commentableAt,
        "country": accountData.country,
        "createdAt": accountData.createdAt,
        "emblemCount": accountData.emblemCount,
        "followerCount": accountData.followerCount,
        "gamerId": accountData.gamerId,
        "homeLevel": accountData.homeLevel,
        "id": accountData.internalId,
        "inventory": {"avatars": json.loads(accountData.inventory).get("avatars")} if accountData.inventory else {},
        "lastLoginAt": accountData.lastLoginAt,
        "levelCount": accountData.levelCount,
        "nickname": accountData.nickname,
        "playerPt": accountData.playerPt,
        "researches": accountData.researches,
        "visibleAt": accountData.visibleAt
        }
    
    if level >= 2:
        accountToReturn["campaigns"] = json.loads(accountData.campaigns) if accountData.campaigns else {}
        accountToReturn["clearCount"] = accountData.clearCount
        accountToReturn["gem"] = accountData.gem
        accountToReturn["hasUnfinishedIAP"] = accountData.hasUnfinishedIAP
        accountToReturn["inventory"] = json.loads(accountData.inventory) if accountData.inventory else {}
        accountToReturn["lang"] = accountData.lang
        accountToReturn["maxVideoId"] = accountData.maxVideoId
        accountToReturn["nameVersion"] = accountData.nameVersion
        accountToReturn["researches"] = accountData.researches

    if level >= 3:
        accountToReturn["altPassword"] = accountData.altPassword
        accountToReturn["password"] = accountData.password

    return accountToReturn
