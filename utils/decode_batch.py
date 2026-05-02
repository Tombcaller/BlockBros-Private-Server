from models import Level

def decode_batch(batch):

    if not batch:
        return
    
    #§ If "level" key in batch, update play counts §#
    if batch.get("level"):
        for levelId in batch["level"].items():
            Level.query.filter_by(internalId=levelId).first().playCount += batch["level"][str(levelId)]["play"]
    
    #§ KELIXE, please can you add the rest of the level batch decoding here when you have time? §#
    #§ HTTP interception still is not working on my phone unfortunately so cannot do myself  :( §#    
    