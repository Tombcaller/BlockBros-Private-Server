from models import Level

def decode_batch(batch):

    if not batch:
        return
    
    #§ If "level" key in batch, update play counts §#
    if batch.get("level"):
        for levelId, data in batch["level"].items():
            level = Level.query.filter_by(internalId=levelId).first()
            if level: level.playCount += data["play"]
