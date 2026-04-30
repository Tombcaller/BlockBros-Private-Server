from models import Level, account

itemReturnLimit = 10
homeFeedItemReturnLimit = 20

GAMER_LIST_TYPES = {
    "active": {
        "query": lambda: account.query.order_by(account.lastLoginAt.desc()),
        "cursor_field": "lastLoginAt"
    },
    "topPlayer": {
        "query": lambda: account.query.order_by(account.playerPt.desc()),
        "cursor_field": "playerPt"
    },
    "topBuilder": {
        "query": lambda: account.query.order_by(account.builderPt.desc()),
        "cursor_field": "builderPt"
    }
}

LEVEL_LIST_TYPES = {
    "own": {
        "query": lambda internalId: Level.query.filter_by(gamerInternalId=internalId).order_by(Level.createdAt.desc()),
        "cursor_field": "createdAt"
    },
    "new": {
        "query": lambda: Level.query.order_by(Level.createdAt.desc()),
        "cursor_field": "createdAt"
    },
}