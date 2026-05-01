#§ -------- IMPORTS -------- §#
#§ Server Utility Imports §#
from models import Completion, Level, Account, Comment
from utils.cursor import encode_cursor, decode_cursor

#§ Misc Imports §#
import json
import time
#§ ------------------------- §#

#§ Function to get the player data of a user by internalId §#
def get_player_data(internalId, level = 1):
    accountData = Account.query.filter_by(internalId=internalId).first()
    
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
def load_gamer_list_page(baseQuery, cursorField, cursor, limit=10):

    #§ Exclude accounts with 0 or less of the cursor field §#
    baseQuery = baseQuery.filter(getattr(Account, cursorField) > 0)

    #§ Decode cursor from request (If there is one) §#
    if cursor:
        cursor_data = decode_cursor(cursor)

        #§ Grabbing value from cursor to resume list loading from §#
        boundary = cursor_data.get(cursorField)

        #§ If there is a boundary in the cursor, add a filter to the base query §#
        if boundary is not None:
            baseQuery = baseQuery.filter(getattr(Account, cursorField) < boundary)

    #§ Grabbing items from database query §#
    results = baseQuery.limit(limit + 1).all()
    allLoaded = len(results) < limit
    items = results[:limit]

    #§ Encoding a new cursor if not at the last page §#
    nextCursor = None
    if not allLoaded and len(items) > 0:
        nextBoundary = getattr(items[-1], cursorField)
        nextCursor = encode_cursor({
            cursorField: nextBoundary,
            "generated": int(time.time())
        })

    #§ Returning items, next page cursor and all loaded state §#
    return items, nextCursor, allLoaded

#§ Function to load a page of a "level" list from a cursor §#
def load_level_list_page(baseQuery, cursorField, cursor, limit=10):

    #§ Exclude levels with 0 or less of the cursor field §#
    baseQuery = baseQuery.filter(getattr(Level, cursorField) > 0)

    #§ Decode cursor from request (If there is one) §#
    if cursor:
        cursor_data = decode_cursor(cursor)

        #§ Grabbing value from cursor to resume list loading from §#
        boundary = cursor_data.get(cursorField)

        #§ If there is a boundary in the cursor, add a filter to the base query §#
        if boundary is not None:
            baseQuery = baseQuery.filter(getattr(Level, cursorField) < boundary)

    #§ Grabbing items from database query §#
    results = baseQuery.limit(limit + 1).all()
    allLoaded = len(results) < limit
    items = results[:limit]

    #§ Encoding a new cursor if not at the last page §#
    nextCursor = None
    if not allLoaded and len(items) > 0:
        nextBoundary = getattr(items[-1], cursorField)
        nextCursor = encode_cursor({
            cursorField: nextBoundary,
            "generated": int(time.time())
        })

    #§ Returning items, next page cursor and all loaded state §#
    return items, nextCursor, allLoaded

#§ Function to get the data of a comment by internalId §#
def get_comment_data(internalId):
    commentData = Comment.query.filter_by(internalId=internalId).first()

    commentToReturn = {
        "args": json.loads(commentData.args),
        "commentId": commentData.internalId,
        "createdAt": int(commentData.createdAt),
        "gamer": get_player_data(commentData.gamerInternalId),
        "message": commentData.message,
        "type": commentData.messageType 
    }

    return commentToReturn

#§ Function to get the data of a level by internalId §#
def get_level_data(internalId, gamerInternalId = None):
    levelData = Level.query.filter_by(internalId=internalId).first()
    levelCompletionData = Completion.query.filter_by(levelInternalId=internalId, gamerInternalId=gamerInternalId).first() if gamerInternalId else None

    levelToReturn = {
        "clearCount": levelData.clearCount,
        "clearVersion": levelData.clearVersion,
        "commentCount": levelData.commentCount,
        "commentedAt": levelData.commentedAt,
        "config": levelData.config,
        "createdAt": int(levelData.createdAt),
        "difficulty": levelData.difficulty,
        "draft": levelData.draft,
        "gamerInternalId": levelData.gamerInternalId,
        "gamer": get_player_data(levelData.gamerInternalId),
        "id": levelData.internalId,
        "levelId": levelData.levelId,
        "map": levelData.map,
        "playCount": levelData.playCount,
        "rating": levelData.rating,
        "ratingCount": levelData.ratingCount,
        "tag": levelData.tag,
        "theme": levelData.theme,
        "tier": levelData.tier,
        "time": levelCompletionData.completionTime if levelCompletionData else 0,
        "title": levelData.title,
        "todayRating": levelData.todayRating,
        "uuClearCount": levelData.uuClearCount,
        "uuCount": levelData.uuCount,
        "version": levelData.version,
        "yesterdayRating": levelData.yesterdayRating,
    }
    return levelToReturn

def get_completion_data(levelInternalId, gamerInternalId):
    completionData = Completion.query.filter_by(levelInternalId=levelInternalId, gamerInternalId=gamerInternalId).first()
    completionToReturn = {
        "gamerInternalId": completionData.gamerInternalId,
        "levelInternalId": completionData.levelInternalId,
        "completionTime": completionData.completionTime
    }

    return completionToReturn
#§ Function to load a page of a "gamer" list from a cursor §#
def load_comment_list_page(baseQuery, cursorField, cursor, limit=10):

    #§ Decode cursor from request (If there is one) §#
    if cursor:
        cursor_data = decode_cursor(cursor)

        #§ Grabbing value from cursor to resume list loading from §#
        boundary = cursor_data.get(cursorField)

        #§ If there is a boundary in the cursor, add a filter to the base query §#
        if boundary is not None:
            baseQuery = baseQuery.filter(getattr(Comment, cursorField) < boundary)

    #§ Grabbing items from database query §#
    results = baseQuery.limit(limit + 1).all()
    allLoaded = len(results) < limit
    items = results[:limit]

    #§ Encoding a new cursor if not at the last page §#
    nextCursor = None
    if not allLoaded and len(items) > 0:
        nextBoundary = getattr(items[-1], cursorField)
        nextCursor = encode_cursor({
            cursorField: nextBoundary,
            "generated": int(time.time())
        })

    #§ Returning items, next page cursor and all loaded state §#
    return items, nextCursor, allLoaded