import json

config_file_location = "config/config.json"
sc_file_location = "config/secret_config.json"

empty_config = {
  "Prefix": "-",
  "Cogs": [
    "cogs.misc",
    "cogs.osu"
  ],
  "osu_config": {
    "info": "'roles' cannot currently be changed, as it will break the bot. And 'servers' will be set up automatically, with the -reg command.",
    "roles": [
    "0-9k",
    "10-29k",
    "30-49k",
    "50-69k",
    "70-89k",
    "90-99k",
    "100-149k",
    "150-199k",
    "200-499k",
    "500-999k"
    ],
    "servers": {
      }
    }
  }

empty_sc = {
    "TOKEN": "token",
    "osu!api": [
      "client_id",
      "client_secret"
    ]
}


def init():
    try:
        with open(config_file_location, 'x') as config_file:
            with open(config_file_location, 'w') as config_file:
                json.dump(empty_config, config_file, indent=2)
    except:
        pass

    try:
        with open(sc_file_location, 'x') as sc_file:
            with open(sc_file_location, 'w') as sc_file:
                json.dump(empty_sc, sc_file, indent=2)
    except:
        pass
