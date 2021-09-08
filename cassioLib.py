import random
import costanti_api_riot
import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue
from collections import Counter
import requests
import pprint
from costanti_api_riot import *


global match_info
global match_info_riot_API


def getMatchInfoById(id):
    response = requests.get(MATCH_BY_ID.format(id)).json()
    global match_info_riot_API
    match_info_riot_API = response
    return match_info_riot_API


def getParticipants():
    players = []
    for player in match_info.participants:
        players.append(player)
        if len(players) >= 5:
            break
    return players


def getSummonerName(player):
    return player.summoner.name


def getLaneOfPlayer(player):
    info = match_info_riot_API["info"]["participants"]
    for p in info:
        if p["summonerName"] == player.summoner.name:
            if p["teamPosition"] == "JUNGLE":
                return "JUNGLE"
            elif p["teamPosition"] == "TOP":
                return "TOP"
            elif p["teamPosition"] == "MIDDLE":
                return "MID"
            elif p["teamPosition"] == "UTILITY":
                return "SUPPORT"
            elif p["teamPosition"] == "BOTTOM":
                return "ADC"


def getImageOfChampion(player):
    return CHAMPIONS_IMAGE_PREFIX.format(player.champion.image.url)


def getNameOfChampion(player):
    return player.champion.name


def getPatch(player):
    return player.version


def getDurationGame():
    global match_info
    return str(match_info.duration)


def getDate():
    global match_info
    return str(match_info.creation.datetime)[:19]


def getTeamBans(player):
    bans_to_return = ""
    bans = player.team.bans
    for ban in bans:
        bans_to_return += ban.name + " / "
    return bans_to_return


def getEnemyTeamBans(player):
    bans_to_return = ""
    bans = player.enemy_team.bans
    for ban in bans:
        bans_to_return += ban.name + " / "
    return bans_to_return


def getResult(player):
    if player.team.win:
        return "Win"
    else:
        return "Lose"


def getOpponentSummoner(player):
    opponent_name = ""
    for enemy_player in player.enemy_team.participants:
        if getLaneOfPlayer(enemy_player) == getLaneOfPlayer(player):
            opponent_name = enemy_player.summoner.name
            return opponent_name


def getOpponentChampion(player):
    champion_name = ""
    for enemy_player in player.enemy_team.participants:
        if getLaneOfPlayer(enemy_player) == getLaneOfPlayer(player):
            champion_name = enemy_player.champion.name
            return champion_name


def getOpponentChampionImage(player):
    champion_img = ""
    for enemy_player in player.enemy_team.participants:
        if getLaneOfPlayer(enemy_player) == getLaneOfPlayer(player):
            champion_img = CHAMPIONS_IMAGE_PREFIX.format(enemy_player.champion.image.url)
            return champion_img


def getKills(player):
    return player.stats.kills


def getAssists(player):
    return player.stats.assists


def getDeaths(player):
    return player.stats.deaths


def getKDA(player):
    return player.stats.kda


def getCS(player):
    return player.stats.total_minions_killed


def getTotalGold(player):
    return player.stats.gold_earned


def getTotalDamageDealt(player):
    return player.stats.total_damage_dealt_to_champions


def getTotalEXP(player):
    return player.stats.level


def getTotalVisionScore(player):
    return player.stats.vision_score


def getTimeCCOthers(player):
    return player.stats.time_CCing_others


def getFirstBloodAssist(player):
    return player.stats.first_blood_assist


def makeRowForMatch(player):
    return [getSummonerName(player),
            "Link",
            getLaneOfPlayer(player),
            getNameOfChampion(player),
            getImageOfChampion(player),
            getPatch(player),
            getDurationGame(),
            getDate(),
            getTeamBans(player),
            getEnemyTeamBans(player),
            player.side.name,
            getResult(player),
            getOpponentSummoner(player),
            getOpponentChampion(player),
            getOpponentChampionImage(player),
            getKills(player),
            getDeaths(player),
            getAssists(player),
            getKDA(player),
            getCS(player),
            getTotalGold(player),
            getTotalDamageDealt(player),
            getTotalEXP(player),
            getTotalVisionScore(player),
            getTimeCCOthers(player),
            getFirstBloodAssist(player),
            "False?",

            ]


def makeRowsOfMatch(game_id):
    global match_info
    global match_info_riot_API
    cass.set_riot_api_key(API)  # This overrides the value set in your configuration/settings.
    cass.set_default_region("EUW")
    match_info = cass.get_match(int(game_id), 'EUW')
    match_info_riot_API = getMatchInfoById("EUW1_" + game_id)
    players = getParticipants()
    rows = [makeRowForMatch(player) for player in players]
    return [e for e in rows]


if __name__ == "__main__":
    makeRowsOfMatch("5447200150")

# p = match_info.participants[0]
# ban = match_info.teams
# print(p.champion.name, p.runes.keystone.name, *[r.name for r in p.stat_runes])
# print(p.champion.name, p.runes.keystone.name, *[r.name for r in p.runes])
# for skill in p.skill_order:
#     print(skill.keyboard_key.value, end=' > ')
# summoner = cass.get_summoner(name="fallensalvo")
