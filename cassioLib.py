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
global match_timeline


def getMatchInfoById(id):
    response = requests.get(MATCH_BY_ID.format(id)).json()
    global match_info_riot_API
    match_info_riot_API = response


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
    return IMAGE_PREFIX.format(player.champion.image.url)


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
            champion_img = IMAGE_PREFIX.format(enemy_player.champion.image.url)
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


def getSoloKills(player):
    count = 0
    for champion_killed in player.timeline.champion_kills:
        if len(champion_killed.assisting_participants) == 0:
            count += 1
    return count


def getSoloDeaths(player):
    count = 0
    for deaths in player.timeline.champion_deaths:
        if len(deaths.assisting_participants) == 0:
            count += 1
    return count


def getKillParticipation(player):
    total_team_kills = 0
    for team_player in player.team.participants:
        total_team_kills += team_player.stats.kills
    kp = player.stats.kills * 100 / total_team_kills
    return str(kp) + "%"


def getDeathsParticipation(player):
    total_team_deaths = 0
    for team_player in player.team.participants:
        total_team_deaths += team_player.stats.deaths
    dp = player.stats.deaths * 100 / total_team_deaths
    return str(dp) + "%"


def getDamageParticipation(player):
    total_damage_dealt = 0
    for team_player in player.team.participants:
        total_damage_dealt += team_player.stats.total_damage_dealt_to_champions
    dmg = player.stats.total_damage_dealt_to_champions * 100 / total_damage_dealt
    return str(dmg) + "%"


def getGoldParticipation(player):
    total_gold_earned = 0
    for team_player in player.team.participants:
        total_gold_earned += team_player.stats.gold_earned
    gold = player.stats.gold_earned * 100 / total_gold_earned
    return str(gold) + "%"


def getCS15(player):
    # recupero minion a 15 minuti
    first_slice = player.timeline.creeps_per_min_deltas['10-20'] * 5  # minion medi al minuto dal min 10 a 20
    second_slice = player.timeline.creeps_per_min_deltas['0-10'] * 10  # minion medi al minuto dal min 0 al min 10
    return first_slice + second_slice


def getCSDiffDeltas(player):
    value_to_return = 0
    if isinstance(player.timeline.cs_diff_per_min_deltas['10-20'], float):
        value_to_return = "{:0.2f}".format(player.timeline.cs_diff_per_min_deltas['10-20'])
    else:
        value_to_return = player.timeline.cs_diff_per_min_deltas['10-20']
    return value_to_return


def getXP15(player):
    # recupero minion a 15 minuti
    first_slice = player.timeline.xp_per_min_deltas['10-20'] * 5  # minion medi al minuto dal min 10 a 20
    second_slice = player.timeline.xp_per_min_deltas['0-10'] * 10  # minion medi al minuto dal min 0 al min 10
    return first_slice + second_slice


def getXPDiffDeltas(player):
    value_to_return = 0
    if isinstance(player.timeline.xp_diff_per_min_deltas['10-20'], float):
        value_to_return = "{:0.2f}".format(player.timeline.xp_diff_per_min_deltas['10-20'])
    else:
        value_to_return = player.timeline.xp_diff_per_min_deltas['10-20']
    return value_to_return


def getGold15(player):
    # recupero minion a 15 minuti
    first_slice = player.timeline.gold_per_min_deltas['10-20'] * 5  # minion medi al minuto dal min 10 a 20
    second_slice = player.timeline.gold_per_min_deltas['0-10'] * 10  # minion medi al minuto dal min 0 al min 10
    return first_slice + second_slice


def getGoldDiffDeltas(player):
    value_to_return = 0
    for enemy_player in player.enemy_team.participants:
        if getLaneOfPlayer(enemy_player) == getLaneOfPlayer(player):
            if isinstance(player.timeline.cs_diff_per_min_deltas['10-20'], float):
                value_to_return = "{:0.2f}".format(player.timeline.gold_per_min_deltas['10-20'] -
                                                   enemy_player.timeline.gold_per_min_deltas['10-20'])
            else:
                value_to_return = player.timeline.cs_diff_per_min_deltas['10-20'] - \
                                  enemy_player.timeline.gold_per_min_deltas['10-20']
    return value_to_return


def getInfoOfPlayerInMatchId(name):
    info = match_info_riot_API["info"]["participants"]
    for p in info:
        if p["summonerName"] == name:
            return p


def getSkillOrder(player):
    value_to_return = ""
    for skill in player.skill_order:
        value_to_return += skill.keyboard_key.value + ' > '
    return value_to_return


def getParticipantIdInMatchId(name):
    return getInfoOfPlayerInMatchId(name)["participantId"]


def getMatchTimelineInfoById(id):
    global match_timeline
    match_timeline = requests.get(MATCH_TIMELINE_BY_ID.format(id)).json()["info"]


def getItemFromId(id):
    result = requests.get(ITEMS).json()["data"][str(id)]["name"]
    return result


def getBuildPathOfPlayerInMatchId(player):
    participant = getParticipantIdInMatchId(player.summoner.name)
    frames = match_timeline["frames"]
    events = [frame["events"] for frame in frames]
    events = [e for event in events for e in event if
              e["type"] == "ITEM_PURCHASED" and e["participantId"] == participant]
    events = sorted(events, key=lambda e: e["timestamp"])
    build_path = getItemFromId(events[0]["itemId"])
    for event in events[1:]:
        build_path += " > " + getItemFromId(event["itemId"])
    return build_path


def getKeystone(player):
    return IMAGE_PREFIX.format(player.runes.keystone.image.url)


def getFirstFinalBuildItem(player):
    if player.stats.items[0] is not None:
        return IMAGE_PREFIX.format(player.stats.items[0].image.url)
    else:
        return ""


def getSecondFinalBuildItem(player):
    if player.stats.items[1] is not None:
        return IMAGE_PREFIX.format(player.stats.items[1].image.url)
    else:
        return ""


def getThirdFinalBuildItem(player):
    if player.stats.items[2] is not None:
        return IMAGE_PREFIX.format(player.stats.items[2].image.url)
    else:
        return ""


def getFourthFinalBuildItem(player):
    if player.stats.items[3] is not None:
        return IMAGE_PREFIX.format(player.stats.items[3].image.url)
    else:
        return ""


def getFifthFinalBuildItem(player):
    if player.stats.items[4] is not None:
        return IMAGE_PREFIX.format(player.stats.items[4].image.url)
    else:
        return ""


def getSixthFinalBuildItem(player):
    if player.stats.items[5] is not None:
        return IMAGE_PREFIX.format(player.stats.items[5].image.url)
    else:
        return ""


def getFirstRune(player):
    counter = 0
    rune_to_return = None
    for r in player.runes:
        if counter == 1:
            break
        else:
            rune_to_return = IMAGE_PREFIX.format(r.image.url)
            counter += 1
    return rune_to_return


def getSecondRune(player):
    counter = 0
    rune_to_return = None
    for r in player.runes:
        if counter == 2:
            break
        else:
            rune_to_return = IMAGE_PREFIX.format(r.image.url)
            counter += 1
    return rune_to_return


def getThirdRune(player):
    counter = 0
    rune_to_return = None
    for r in player.runes:
        if counter == 3:
            break
        else:
            rune_to_return = IMAGE_PREFIX.format(r.image.url)
            counter += 1
    return rune_to_return


def getFourthRune(player):
    counter = 0
    rune_to_return = None
    for r in player.runes:
        if counter == 4:
            break
        else:
            rune_to_return = IMAGE_PREFIX.format(r.image.url)
            counter += 1
    return rune_to_return


def getFifthRune(player):
    counter = 0
    rune_to_return = None
    for r in player.runes:
        if counter == 5:
            break
        else:
            rune_to_return = IMAGE_PREFIX.format(r.image.url)
            counter += 1
    return rune_to_return


def getSixthRune(player):
    counter = 0
    rune_to_return = None
    for r in player.runes:
        if counter == 6:
            break
        else:
            rune_to_return = IMAGE_PREFIX.format(r.image.url)
            counter += 1
    return rune_to_return


def getWard(player):
    return "Ward"


def checkStatName(name):
    if name == 'Adaptive':
        return 'AdaptiveForce'
    elif name == 'MagicResist':
        return 'MagicRes'
    else:
        return name


def getFirstStat(player):
    counter = 0
    rune_to_return = None
    for r in player.stat_runes:
        if counter == 1:
            break
        else:
            name = r.name
            name = checkStatName(name)
            rune_to_return = IMAGE_PREFIX.format(r.path.image_url + BUILD_RUNE_STATS_IMAGE.format(name))
            counter += 1
    return rune_to_return


def getSecondStat(player):
    counter = 0
    rune_to_return = None
    for r in player.stat_runes:
        if counter == 2:
            break
        else:
            name = r.name
            name = checkStatName(name)
            rune_to_return = IMAGE_PREFIX.format(r.path.image_url + BUILD_RUNE_STATS_IMAGE.format(name))
            counter += 1
    return rune_to_return


def getThirdStat(player):
    counter = 0
    rune_to_return = None
    for r in player.stat_runes:
        if counter == 3:
            break
        else:
            name = r.name
            name = checkStatName(name)
            rune_to_return = IMAGE_PREFIX.format(r.path.image_url + BUILD_RUNE_STATS_IMAGE.format(name))
            counter += 1
    return rune_to_return


def isFirstDrake(player):
    return str(player.team.first_dragon).upper()


def isFirstHerald(player):
    return str(player.team.first_rift_herald).upper()


def isFirstBaron(player):
    return str(player.team.first_baron).upper()


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
            getSoloKills(player),
            getSoloDeaths(player),
            getKillParticipation(player),
            getDeathsParticipation(player),
            getDamageParticipation(player),
            getGoldParticipation(player),
            getCS15(player),
            getCSDiffDeltas(player),
            getXP15(player),
            getXPDiffDeltas(player),
            getGold15(player),
            getGoldDiffDeltas(player),
            "",
            getSkillOrder(player),
            "",
            getBuildPathOfPlayerInMatchId(player),
            "",
            getFirstFinalBuildItem(player),
            getSecondFinalBuildItem(player),
            getThirdFinalBuildItem(player),
            getFourthFinalBuildItem(player),
            getFifthFinalBuildItem(player),
            getSixthFinalBuildItem(player),
            getWard(player),
            getKeystone(player),
            getSecondRune(player),
            getThirdRune(player),
            getFourthRune(player),
            getFifthRune(player),
            getSixthRune(player),
            getFirstStat(player),
            getSecondStat(player),
            getThirdStat(player),
            isFirstDrake(player),
            isFirstHerald(player),
            isFirstBaron(player)
            ]


def makeRowsOfMatch(game_id):
    global match_info
    cass.set_riot_api_key(API)  # This overrides the value set in your configuration/settings.
    cass.set_default_region("EUW")
    match_info = cass.get_match(int(game_id), 'EUW')
    getMatchInfoById("EUW1_" + game_id)
    getMatchTimelineInfoById("EUW1_" + game_id)
    players = getParticipants()
    rows = [makeRowForMatch(player) for player in players]
    return [e for e in rows]


if __name__ == "__main__":
    makeRowsOfMatch("5454525634")

# p = match_info.participants[0]
# ban = match_info.teams
# print(p.champion.name, p.runes.keystone.name, *[r.name for r in p.stat_runes])
# print(p.champion.name, p.runes.keystone.name, *[r.name for r in p.runes])
# for skill in p.skill_order:
#     print(skill.keyboard_key.value, end=' > ')
# summoner = cass.get_summoner(name="fallensalvo")
