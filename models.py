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
    createdAt = db.Column(db.Integer)
    emblemCount = db.Column(db.Integer)
    followerCount = db.Column(db.Integer)
    gamerId = db.Column(db.Integer, primary_key=True)
    gem = db.Column(db.Integer)
    hasUnfinishedIAP = db.Column(db.Integer)
    homeLevel = db.Column(db.String)
    internalId = db.Column(db.Integer, unique=True)
    inventory = db.Column(db.String)
    lang = db.Column(db.String)
    lastLoginAt = db.Column(db.Integer)
    levelCount = db.Column(db.Integer)
    maxVideoId = db.Column(db.Integer)
    nameVersion = db.Column(db.Integer)
    nickname = db.Column(db.String)
    password = db.Column(db.String)
    playerPt = db.Column(db.Integer)
    researches = db.Column(db.String)
    token = db.Column(db.String)
    visibleAt = db.Column(db.Integer)