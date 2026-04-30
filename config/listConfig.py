from models import Account

itemReturnLimit = 10
homeFeedItemReturnLimit = 20

GAMER_LIST_TYPES = {
    "active": {
        "query": lambda: Account.query.order_by(Account.lastLoginAt.desc()),
        "cursor_field": "lastLoginAt"
    },
    "topPlayer": {
        "query": lambda: Account.query.order_by(Account.playerPt.desc()),
        "cursor_field": "playerPt"
    },
    "topBuilder": {
        "query": lambda: Account.query.order_by(Account.builderPt.desc()),
        "cursor_field": "builderPt"
    }
}