import requests
import json

sc_file_location = "config/secret_config.json"
with open(sc_file_location, "r") as sc_file:
    sc = json.load(sc_file)

client_id = sc["osu!api"][0]
client_secret = sc["osu!api"][1]

data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials',
    'scope': 'public'
}

auth = requests.post("https://osu.ppy.sh/oauth/token", data=data).json()
print(auth)