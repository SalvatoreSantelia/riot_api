import requests
from costanti_api_riot import *
from datetime import datetime
import tzlocal  # $ pip install tzlocal
import cassiopeia as cass
import time

playerInfo = ""
matchesIdOfPlayer = ""
matchInfo = ""


def getPlayerInfo(name):
    response = requests.get(SUMMONER.format(name)).json()
    global playerInfo
    playerInfo = response
    return response


def getMatchesIdOfPlayer(name, num_matches):
    player_puuid = playerInfo["puuid"]
    response = requests.get(MATCHES_ID_BY_PUUID.format(player_puuid, 0, num_matches)).json()
    global matchesIdOfPlayer
    matchesIdOfPlayer = response
    return response


def getSummonerName(name):
    return getInfoOfPlayerInMatchId(name)["summonerName"]


def getMatchInfoById(id):
    response = requests.get(MATCH_BY_ID.format(id)).json()
    global matchInfo
    matchInfo = response
    return matchInfo


def getPatchOfMatchId():
    return matchInfo["info"]["gameVersion"][0:5]


def getDateOfMatchId():
    unixDate = matchInfo["info"]["gameStartTimestamp"]
    unix_timestamp = float(int(str(unixDate)[:10]))
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    return str(local_time)


def getDurationMatchId():
    millis = matchInfo["info"]["gameDuration"]
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    duration = "%d:%d:%d" % (hours, minutes, seconds)
    return duration


def getInfoOfPlayerInMatchId(name):
    info = matchInfo["info"]["participants"]
    for p in info:
        if p["summonerName"] == name:
            return p


def getPlayersInMatchId():
    names = []
    for i in range(5):
        names.append(matchInfo["info"]["participants"][i]["summonerName"])
    return names


def getChampionOfPlayerInMatchId(name):
    return getInfoOfPlayerInMatchId(name)["championName"]


def getRoleOfPlayerInMatchId(name):
    return getInfoOfPlayerInMatchId(name)["teamPosition"]


'''
def getOpponentChampionOfPlayerInMatchId(name, id):
    info = getInfoOfPlayerInMatchId(name, id)
    role = info[""]
    '''


def hasPlayerWonInMatchId(name):
    if getInfoOfPlayerInMatchId(name)["win"]: return "W"
    return "L"


def getKillsOfPlayerInMatchId(name):
    return getInfoOfPlayerInMatchId(name)["kills"]


def getDeathsOfPlayerInMatchId(name):
    return getInfoOfPlayerInMatchId(name)["deaths"]


def getAssistsOfPlayerInMatchId(name):
    return getInfoOfPlayerInMatchId(name)["assists"]


def getKDAOfPlayerInMatchId(name):
    return "{:0.2f}".format((getKillsOfPlayerInMatchId(name) +
                             getAssistsOfPlayerInMatchId(name)) / getDeathsOfPlayerInMatchId(name))


def getParticipantIdInMatchId(name):
    return getInfoOfPlayerInMatchId(name)["participantId"]


def getMatchTimelineInfoById(id):
    return requests.get(MATCH_TIMELINE_BY_ID.format(id)).json()["info"]


def getItemFromId(id):
    result = requests.get(ITEMS).json()["data"][str(id)]["name"]
    return result


def skillSlotToChar(slot):
    if slot == 1: return "Q"
    if slot == 2: return "W"
    if slot == 3: return "E"
    if slot == 4: return "R"


def getSkillOrderOfPlayerInMatchId(name, game_id):
    participantId = getParticipantIdInMatchId(name)
    frames = getMatchTimelineInfoById(game_id)["frames"]
    events = [frame["events"] for frame in frames]
    events = [e for event in events for e in event if
              e["type"] == "SKILL_LEVEL_UP" and e["participantId"] == participantId]
    skills = [skillSlotToChar(e["skillSlot"]) for e in sorted(events, key=lambda e: e["timestamp"])]
    skill_order = skills[0]
    for skill in skills[1:]:
        skill_order += " > " + skill
    return skill_order


def getBuildPathOfPlayerInMatchId(name, game_id):
    participantId = getParticipantIdInMatchId(name)
    frames = getMatchTimelineInfoById(game_id)["frames"]
    events = [frame["events"] for frame in frames]
    events = [e for event in events for e in event if
              e["type"] == "ITEM_PURCHASED" and e["participantId"] == participantId]
    events = sorted(events, key=lambda e: e["timestamp"])
    build_path = getItemFromId(events[0]["itemId"])
    for event in events[1:]:
        build_path += " > " + getItemFromId(event["itemId"])
    return build_path


def getBanOfMatchId():
    bansToReturn = ""
    teamBans = matchInfo["info"]["teams"][0]["bans"]
    for ban in teamBans:
        banId = ban["championId"]
        data = requests.get(CHAMPIONS).json()["data"]
        for champ, champInfo in data.items():  # accedo al dizionario dei champs
            if champInfo["key"] == str(banId):
                bansToReturn += champInfo["name"] + ' / '
    return bansToReturn


def getOppositeTeamBanOfMatchId():
    bansToReturn = ""
    teamBans = matchInfo["info"]["teams"][1]["bans"]
    for ban in teamBans:
        banId = ban["championId"]
        data = requests.get(CHAMPIONS).json()["data"]
        for champ, champInfo in data.items():  # accedo al dizionario dei champs
            if champInfo["key"] == str(banId):
                bansToReturn += champInfo["name"] + ' / '
    return bansToReturn


def getGoldEarndInMatchWithIdByPlayer(name):
    return getInfoOfPlayerInMatchId(name)["goldEarned"]


def getTotalDamageDealtInMatchWithIdByPlayer(name):
    return getInfoOfPlayerInMatchId(name)["totalDamageDealt"]


def getCsFarmaedInMatchWithIdByPlayer(name, id):
    return getInfoOfPlayerInMatchId(name, id)["totalMinionsKilled"] + getInfoOfPlayerInMatchId(name, id)[
        "neutralMinionsKilled"]


def getChampImage(champName):
    result = CHAMPIONS_IMAGE_PREFIX.format(champName)
    return result


def makeSpreadSheetRowForMatchIdOfPlayer(name, game_id):
    getPlayerInfo(name)
    champName = getChampionOfPlayerInMatchId(name)
    return [getSummonerName(name), "Link?",
            getRoleOfPlayerInMatchId(name),
            champName,
            getChampImage(champName),
            getPatchOfMatchId(),
            getDurationMatchId(),
            getDateOfMatchId(),
            getBanOfMatchId(),
            getOppositeTeamBanOfMatchId(),
            hasPlayerWonInMatchId(name),
            getKillsOfPlayerInMatchId(name),
            getDeathsOfPlayerInMatchId(name),
            getAssistsOfPlayerInMatchId(name),
            getKDAOfPlayerInMatchId(name),
            getGoldEarndInMatchWithIdByPlayer(name),
            getTotalDamageDealtInMatchWithIdByPlayer(name),
            getSkillOrderOfPlayerInMatchId(name, game_id),
            getBuildPathOfPlayerInMatchId(name, game_id)]


def makeSpreadSheetRowsOfPlayer(game_id):
    getMatchInfoById(game_id)  # recupero info del match una sola volta
    names = getPlayersInMatchId()  # recupera tutti i giocatori di un dato game
    rows = [(print(name), makeSpreadSheetRowForMatchIdOfPlayer(name, game_id)) for name in names]
    return [e[1] for e in rows]
