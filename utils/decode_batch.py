from models import Account, Level, Interactions, db
from utils.db_item_factory import build_interaction
from utils.get_db_data import get_player_rank


def decode_batch(batch, loggedInId):
    if not batch: return

    #§ "level" treatment §#
    if batch.get("level"):
        for levelIdStr, levelData in batch["level"].items():
            #§ Grabbing level from database to edit values §#
            levelId = int(levelIdStr)
            level = Level.query.filter_by(internalId=levelId).first()

            # grab existing interaction. if not existing, create one. #
            interaction = Interactions.query.filter_by(levelInternalId=levelId,gamerInternalId=loggedInId).first()
            if not interaction:
                db.session.add(build_interaction(levelInternalId=levelId,gamerInternalId=loggedInId,completionTime=0,givenRating=-1,fav=0))

            #§ Adding play, clear, rating, fav data to level and interaction models §#
            if levelData.get("play"):
                level.playCount += levelData["play"]
            if levelData.get("clear"):
                level.clearCount += levelData["clear"]
            if levelData.get("rating"):
                if interaction.givenRating != -1: #if user already rated, ignore new rating
                    continue
                level.rating += levelData["rating"] * get_player_rank(loggedInId) # rating increases with player rank in 3s
                interaction.givenRating = levelData["rating"]
            if levelData.get("fav"):
                if levelData["fav"] == True:
                    level.favCount += 1
                elif levelData["fav"] == False:
                    level.favCount -= 1
                interaction.fav = levelData["fav"]

    #§ "gamer" treatment §#
    if batch.get("gamer"):
        gamerData = batch["gamer"]
        account = Account.query.filter_by(internalId=loggedInId).first()

        if gamerData.get("avatar"):
            account.avatar = gamerData["avatar"]
        if gamerData.get("lang"):
            account.lang = gamerData["lang"]
        if gamerData.get("homeLevel"):
            account.homeLevel = gamerData["homeLevel"]
        if gamerData.get("video"):
            account.video = gamerData["video"]

    #§ "campaign" treatment needs campaign model i think §#




    db.session.commit()
