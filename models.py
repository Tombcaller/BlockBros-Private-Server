from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

class PingLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Float, default=time.time)

class account(db.Model):
    adminLevel = db.Column(db.Integer)
    altPassword = db.Column(db.String)
    avatar = db.Column(db.Integer)
    builderPt = db.Column(db.Integer)
    campaigns = db.Column(db.String)
    channel = db.Column(db.String)
    clearCount = db.Column(db.Integer)
    commentableAt = db.Column(db.Integer)
    country = db.Column(db.String)
    createdAt = db.Column(db.Float)
    emblemCount = db.Column(db.Integer)
    followerCount = db.Column(db.Integer)
    gamerId = db.Column(db.Integer, primary_key=True)
    gem = db.Column(db.Integer)
    hasUnfinishedIAP = db.Column(db.Integer)
    homeLevel = db.Column(db.String)
    internalId = db.Column(db.Integer, unique=True)
    inventory = db.Column(db.String)
    lang = db.Column(db.String)
    lastLoginAt = db.Column(db.Float)
    levelCount = db.Column(db.Integer)
    maxVideoId = db.Column(db.Integer)
    nameVersion = db.Column(db.Integer)
    nickname = db.Column(db.String)
    password = db.Column(db.String)
    playerPt = db.Column(db.Integer)
    researches = db.Column(db.String)
    token = db.Column(db.String)
    visibleAt = db.Column(db.Integer)

class comment(db.Model):
    messageType = db.Column(db.String, default="plain")
    groupKey = db.Column(db.String, default="feed")
    internalId = db.Column(db.Integer, primary_key=True, unique=True)
    args = db.Column(db.String, default={})
    createdAt = db.Column(db.Integer, default=0)
    gamerInternalId = db.Column(db.Integer)
    message = db.Column(db.String)
    
class Level(db.Model):
    internalId = db.Column(db.Integer)
    levelId = db.Column(db.Integer, primary_key=True)

    gamerInternalId = db.Column(db.Integer)

    clearCount = db.Column(db.Integer)
    clearVersion = db.Column(db.Integer)
    commentCount = db.Column(db.Integer)
    commentedAt = db.Column(db.Integer)
    config = db.Column(db.JSON)
    createdAt = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    draft = db.Column(db.Integer)

    map = db.Column(db.JSON)

    playCount = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    ratingCount = db.Column(db.Integer)
    tag = db.Column(db.String)
    theme = db.Column(db.Integer)
    tier = db.Column(db.Integer)
    time = db.Column(db.Integer)
    title = db.Column(db.String)

    todayRating = db.Column(db.Integer)
    uuClearCount = db.Column(db.Integer)
    uuCount = db.Column(db.Integer)
    version = db.Column(db.Integer)
    yesterdayRating = db.Column(db.Integer)
