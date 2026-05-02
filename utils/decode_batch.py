from models import Level, Interactions, db
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
                interaction = build_interaction(levelInternalId=levelId,gamerInternalId=loggedInId,completionTime=0,givenRating=-1,fav=0)
                db.session.add(interaction)

            #§ Adding play, clear and rating data to level and interaction models §#
            if levelData.get("play"):
                level.playCount += levelData["play"]
            if levelData.get("clear"):
                level.clearCount += levelData["clear"]
            if levelData.get("rating"):

                if interaction.givenRating != -1: #if user already rated, ignore new rating
                    continue
                
                level.rating += levelData["rating"] * get_player_rank(loggedInId) # rating increases with player rank in 3s
                interaction.givenRating = levelData["rating"]

    db.session.commit()
