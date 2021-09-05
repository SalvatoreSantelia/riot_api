import random
import costanti_api_riot
import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue
from collections import Counter
import pprint
from costanti_api_riot import *

global match_info


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
    return player.lane.value


def getImageOfChampion(player):
    return CHAMPIONS_IMAGE_PREFIX.format(player.champion.image.url)


def getNameOfChampion(player):
    return player.champion.name


def makeRowForMatch(player):
    return [getSummonerName(player),
            "Link",
            getLaneOfPlayer(player),
            getNameOfChampion(player),
            getImageOfChampion(player)]


def makeRowsOfMatch(game_id):
    global match_info
    cass.set_riot_api_key(API)  # This overrides the value set in your configuration/settings.
    cass.set_default_region("EUW")
    match_info = cass.get_match(int(game_id), 'EUW')
    players = getParticipants()
    rows = [makeRowForMatch(player) for player in players]
    return [e for e in rows]















# p = match_info.participants[0]
# ban = match_info.teams
# print(p.champion.name, p.runes.keystone.name, *[r.name for r in p.stat_runes])
# print(p.champion.name, p.runes.keystone.name, *[r.name for r in p.runes])
# for skill in p.skill_order:
#     print(skill.keyboard_key.value, end=' > ')
# summoner = cass.get_summoner(name="fallensalvo")