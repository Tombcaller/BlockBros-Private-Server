from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

class PingLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Float, default=time.time)

class account(db.Model):
    gamerId = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=True)
    nickname = db.Column(db.String(10))
    password = db.Column(db.String)
    altPassword = db.Column(db.String)

    inventory = db.Column(db.String)

    homeLevel = db.Column(db.String)

    avatar = db.Column(db.Integer)
    builderPt = db.Column(db.Integer)
    playerPt = db.Column(db.Integer)
    clearCount = db.Column(db.Integer)
    channel = db.Column(db.String)
    country = db.Column(db.String)
    nameVersion = db.Column(db.Integer)
    lang = db.Column(db.String)
    levelCount = db.Column(db.Integer)
    gem = db.Column(db.Integer)
    followerCount = db.Column(db.Integer)
    emblemCount = db.Column(db.Integer)

    createdAt = db.Column(db.Integer)
    lastLoginAt = db.Column(db.Integer)
    commentableAt = db.Column(db.Integer)
    visibleAt = db.Column(db.Integer)

    adminLevel = db.Column(db.Integer)
    maxVideoId = db.Column(db.Integer)
    
    token = db.Column(db.String)