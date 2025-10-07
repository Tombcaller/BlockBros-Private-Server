#§ -------- IMPORTS -------- §#
#§ Server Utility Imports §#
from models import account

#§ Misc Imports §#
import json
#§ ------------------------- §#

def getPublicPlayerData(internalId):
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
        "id": accountData.internalId,
        "inventory": json.loads(accountData.inventory).get("avatars") if accountData.inventory else {},
        "lastLoginAt": accountData.lastLoginAt,
        "levelCount": accountData.levelCount,
        "nickname": accountData.nickname,
        "playerPt": accountData.playerPt,
        "researches": accountData.researches,
        "visibleAt": accountData.visibleAt
        }
    
    return accountToReturn



def getPrivatePlayerData(internalId):
    accountData = account.query.filter_by(internalId=internalId).first()

    accountToReturn = {
        "adminLevel": accountData.adminLevel,
        "altPassword": accountData.altPassword,
        "avatar": accountData.avatar,
        "builderPt": accountData.builderPt,
        "campaigns": json.loads(accountData.campaigns) if accountData.campaigns else {},
        "channel": accountData.channel,
        "clearCount": accountData.clearCount,
        "commentableAt": accountData.commentableAt,
        "country": accountData.country,
        "createdAt": accountData.createdAt,
        "emblemCount": accountData.emblemCount,
        "followerCount": accountData.followerCount,
        "gamerId": accountData.gamerId,
        "gem": accountData.gem,
        "hasUnfinishedIAP": accountData.hasUnfinishedIAP,
        "id": accountData.internalId,
        "inventory": json.loads(accountData.inventory) if accountData.inventory else {},
        "lang": accountData.lang,
        "lastLoginAt": accountData.lastLoginAt,
        "levelCount": accountData.levelCount,
        "maxVideoId": accountData.maxVideoId,
        "nameVersion": accountData.nameVersion,
        "nickname": accountData.nickname,
        "playerPt": accountData.playerPt,
        "researches": accountData.researches,
        "visibleAt": accountData.visibleAt
    }

    return accountToReturn
