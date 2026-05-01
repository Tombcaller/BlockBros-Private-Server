from models import Level, Account

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

clearRewardList = {
      "1": [
        {
          "difficulty": 1,
          "type": "block",
          "id": 4,
          "weight": 30,
          "quantity": 2
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 3,
          "weight": 5,
          "quantity": 1
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 5,
          "weight": 15,
          "quantity": 1
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 6,
          "weight": 15,
          "quantity": 1
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 7,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 8,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 9,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 11,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 13,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 1,
          "type": "block",
          "id": 14,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 1,
          "type": "gem",
          "id": 0,
          "weight": 5,
          "quantity": 1
        }
      ],
      "2": [
        {
          "difficulty": 2,
          "type": "block",
          "id": 4,
          "weight": 30,
          "quantity": 5
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 3,
          "weight": 5,
          "quantity": 2
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 5,
          "weight": 15,
          "quantity": 3
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 6,
          "weight": 15,
          "quantity": 3
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 7,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 8,
          "weight": 5,
          "quantity": 1
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 9,
          "weight": 5,
          "quantity": 1
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 11,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 13,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 2,
          "type": "block",
          "id": 14,
          "weight": 0,
          "quantity": 0
        },
        {
          "difficulty": 2,
          "type": "gem",
          "id": 0,
          "weight": 5,
          "quantity": 2
        }
      ],
      "3": [
        {
          "difficulty": 3,
          "type": "block",
          "id": 4,
          "weight": 10,
          "quantity": 10
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 3,
          "weight": 10,
          "quantity": 3
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 5,
          "weight": 10,
          "quantity": 6
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 6,
          "weight": 10,
          "quantity": 6
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 7,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 8,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 9,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 11,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 13,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 14,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 15,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 16,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 17,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 18,
          "weight": 10,
          "quantity": 4
        },
        {
          "difficulty": 3,
          "type": "gem",
          "id": 0,
          "weight": 10,
          "quantity": 3
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 16,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 17,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 3,
          "type": "block",
          "id": 18,
          "weight": 10,
          "quantity": 8
        }
      ],
      "4": [
        {
          "difficulty": 4,
          "type": "block",
          "id": 4,
          "weight": 10,
          "quantity": 20
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 3,
          "weight": 10,
          "quantity": 6
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 5,
          "weight": 10,
          "quantity": 12
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 6,
          "weight": 10,
          "quantity": 12
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 7,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 8,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 9,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 11,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 13,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 14,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 4,
          "type": "block",
          "id": 15,
          "weight": 10,
          "quantity": 8
        },
        {
          "difficulty": 4,
          "type": "gem",
          "id": 0,
          "weight": 10,
          "quantity": 6
        }
      ]
    }