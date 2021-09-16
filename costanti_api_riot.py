API_KEY = "api_key=RGAPI-70379c7e-e520-4c2b-b279-8ea1f7d8725b"
API = "RGAPI-70379c7e-e520-4c2b-b279-8ea1f7d8725b"
# query
SUMMONER = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{0}?" + API_KEY
MATCHES_ID_BY_PUUID = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?start={1}&count={2}&" + API_KEY
MATCH_BY_ID = "https://europe.api.riotgames.com/lol/match/v5/matches/{0}?" + API_KEY
MATCH_TIMELINE_BY_ID = "https://europe.api.riotgames.com/lol/match/v5/matches/{0}/timeline?" + API_KEY

# assets
ITEMS = "http://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/item.json"
ITEM_IMAGE_PREFIX = '=Image("http://ddragon.leagueoflegends.com/cdn/11.17.1/img/item/{0}", 1)'  # da aggiungere il nome immagine item es 1001.png

CHAMPIONS = "http://ddragon.leagueoflegends.com/cdn/11.17.1/data/en_US/champion.json"

IMAGE_PREFIX = '=Image("{0}", 1)'  # da aggiungre nome champ es Aatrox

BUILD_RUNE_STATS_IMAGE = 'StatMods/StatMods{0}Icon.png'
