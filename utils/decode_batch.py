from models import Account, Level, Interactions, db
from utils.db_item_factory import build_interaction
import time

# REALLLLLLLY BAD CODE AS OF RIGHT NOW !!! #

def decode_batch(batch, loggedInId):
    if not batch:
        return

    #§ "level" treatment §#
    if batch.get("level"):
        for levelIdStr, levelData in batch["level"].items():
            levelId = int(levelIdStr)
            # grab existing interaction. if not existing, create one. #
            interaction = Interactions.query.filter_by(levelInternalId=levelId,gamerInternalId=loggedInId).first()
            if not interaction:
                interaction = build_interaction(levelInternalId=levelId,gamerInternalId=loggedInId,completionTime=0,givenRating=-1,fav=0)
                db.session.add(interaction)

            level = Level.query.filter_by(internalId=levelId).first()

            if levelData.get("play"):
                level.playCount += levelData["play"]
            if levelData.get("clear"):
                level.clearCount += levelData["clear"]
            if levelData.get("rating"):
                account = Account.query.filter_by(internalId=loggedInId).first()
                level.rating += levelData["rating"] * Account.query.filter_by(internalId=loggedInId).first().rank
                interaction.givenRating = levelData["rating"]
    db.session.commit()