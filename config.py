from models import Level, Account

#§ General server settings §#
serverConfig = {
    "port": 8108,
    "debug": True,
    "host": "0.0.0.0",
    "db_name": "data.db"
}
#§ ----------------------- §#

#§ BlockBros server settings §#
mainConfig = {
  "versionLoading": {
    "enabled": False,
    "version": 270
  },
  "adminOverride": {
    "enabled": True,
    "password": "a"
  }
}
#§ ----------------------- §#

#§ List response config §#
listConfig = {
    
  "itemReturnLimit": 10,
  "homeFeedItemReturnLimit": 20,

  "gamerListTypes": {
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
  },
  "levelListTypes": {
      "own": {
          "query": lambda internalId: Level.query.filter_by(gamerInternalId=internalId).order_by(Level.createdAt.desc()),
          "cursor_field": "createdAt"
      },
      "new": {
          "query": lambda: Level.query.order_by(Level.createdAt.desc()),
          "cursor_field": "createdAt"
      },
  }
}
#§ ----------------------- §#

#§ Default account settings §#
defaultAccount = {
	"adminLevel": 0,
 	"avatar": 1,
	"builderPt": 0,
	"campaigns": "{}",
	"channel": "",
	"clearCount": 0,
	"commentableAt": 0,
	"country": "ZZ",
	"emblemCount": 0,
	"followerCount": 0,
	"gem": 100,
	"hasUnfinishedIAP": None,
	"homeLevel": None,
	"lang": "en",
	"levelCount": 0,
	"maxVideoId": 0,
	"nameVersion": 0,
	"nickname": None,
	"playerPt": 0,
	"researches": None,
  "inventory": "{\"blocks\":{\"4\": 100, \"5\": 20, \"6\": 20, \"7\": 5, \"8\": 1, \"9\": 3}, \"avatars\":[1], \"themes\":{\"1\": 1}}"
}
#§ ----------------------- §#

#§ Level reward settings §#
clearRewardList = {
      "1": [
        {
          "type": "block",
          "id": 4,
          "quantity": 2
        },
        {
          "type": "block",
          "id": 3,
          "quantity": 1
        },
        {
          "type": "block",
          "id": 5,
          "quantity": 1
        },
        {
          "type": "block",
          "id": 6,
          "quantity": 1
        },
        {
          "type": "gem",
          "id": 0,
          "quantity": 1
        }
      ],
      "2": [
        {
          "type": "block",
          "id": 4,
          "quantity": 5
        },
        {
          "type": "block",
          "id": 3,
          "quantity": 2
        },
        {
          "type": "block",
          "id": 5,
          "quantity": 3
        },
        {
          "type": "block",
          "id": 6,
          "quantity": 3
        },
        {
          "type": "block",
          "id": 8,
          "quantity": 1
        },
        {
          "type": "block",
          "id": 9,
          "quantity": 1
        },
        {
          "type": "gem",
          "id": 0,
          "quantity": 2
        }
      ],
      "3": [
        {
          "type": "block",
          "id": 4,
          "quantity": 10
        },
        {
          "type": "block",
          "id": 3,
          "quantity": 3
        },
        {
          "type": "block",
          "id": 5,
          "quantity": 6
        },
        {
          "type": "block",
          "id": 6,
          "quantity": 6
        },
        {
          "type": "block",
          "id": 7,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 8,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 9,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 11,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 13,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 14,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 15,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 16,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 17,
          "quantity": 4
        },
        {
          "type": "block",
          "id": 18,
          "quantity": 4
        },
        {
          "type": "gem",
          "id": 0,
          "quantity": 3
        },
        {
          "type": "block",
          "id": 16,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 17,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 18,
          "quantity": 8
        }
      ],
      "4": [
        {
          "type": "block",
          "id": 4,
          "quantity": 20
        },
        {
          "type": "block",
          "id": 3,
          "quantity": 6
        },
        {
          "type": "block",
          "id": 5,
          "quantity": 12
        },
        {
          "type": "block",
          "id": 6,
          "quantity": 12
        },
        {
          "type": "block",
          "id": 7,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 8,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 9,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 11,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 13,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 14,
          "quantity": 8
        },
        {
          "type": "block",
          "id": 15,
          "quantity": 8
        },
        {
          "type": "gem",
          "id": 0,
          "quantity": 6
        }
      ]
    }
#§ ----------------------- §#