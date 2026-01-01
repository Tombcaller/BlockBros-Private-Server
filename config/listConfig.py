from models import account, comment

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