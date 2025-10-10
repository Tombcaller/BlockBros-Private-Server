from models import account

itemReturnLimit = 10

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