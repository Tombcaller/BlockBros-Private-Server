#§ -------- IMPORTS -------- §#
#§ Server Utility Imports §#
from models import account
from utils.cursor import encode_cursor, decode_cursor

#§ Misc Imports §#
import json
import time
#§ ------------------------- §#

#§ Function to get the player data of a user by internalId §#
def getPlayerData(internalId, level = 1):
    accountData = account.query.filter_by(internalId=internalId).first()

    accountToReturn = {
        "adminLevel": accountData.adminLevel,
        "avatar": accountData.avatar,
        "builderPt": accountData.builderPt,
        "channel": accountData.channel,
        "commentableAt": accountData.commentableAt,
        "country": accountData.country,
        "createdAt": int(accountData.createdAt),
        "emblemCount": accountData.emblemCount,
        "followerCount": accountData.followerCount,
        "gamerId": accountData.gamerId,
        "homeLevel": accountData.homeLevel,
        "id": accountData.internalId,
        "inventory": {"avatars": json.loads(accountData.inventory).get("avatars")} if accountData.inventory else {},
        "lastLoginAt": int(accountData.lastLoginAt),
        "levelCount": accountData.levelCount,
        "nickname": accountData.nickname,
        "playerPt": accountData.playerPt,
        "researches": accountData.researches,
        "visibleAt": accountData.visibleAt
        }
    
    #§ If requested, higher/more secretive levels of information can be returned §#
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



#§ Function to load a page of a "gamer" list from a cursor §#
def loadGamerListPage(base_query, cursor_field, cursor, limit=10):

    #§ Exclude accounts with 0 or less of the cursor field §#
    base_query = base_query.filter(getattr(account, cursor_field) > 0)

    #§ Decode cursor from request (If there is one) §#
    if cursor:
        cursor_data = decode_cursor(cursor)

        #§ Grabbing value from cursor to resume list loading from §#
        boundary = cursor_data.get(cursor_field)

        #§ If there is a boundary in the cursor, add a filter to the base query §#
        if boundary is not None:
            base_query = base_query.filter(getattr(account, cursor_field) < boundary)

    #§ Grabbing items from database query §#
    results = base_query.limit(limit + 1).all()
    allLoaded = len(results) < limit
    items = results[:limit]

    #§ Encoding a new cursor if not at the last page §#
    nextCursor = None
    if not allLoaded and len(items) > 0:
        nextBoundary = getattr(items[-1], cursor_field)
        nextCursor = encode_cursor({
            cursor_field: nextBoundary,
            "generated": int(time.time())
        })

    #§ Returning items, next page cursor and all loaded state §#
    return items, nextCursor, allLoaded
