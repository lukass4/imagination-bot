import requests
import json
from pprint import pprint
import math
from mojang import MojangAPI

answer = input("Player: ")
uuid = MojangAPI.get_uuid(answer)
url = f"https://api.hypixel.net/player?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&uuid={uuid}"
DATA = requests.get(url).json()

def sw_xp_to_lvl(xp):
    xps = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
    if xp >= 15000:
        return (xp - 15000) / 10000. + 12
    else:
        for i in range(len(xps)):
            if xp < xps[i]:
                return i + float(xp - xps[i-1]) / (xps[i] - xps[i-1])

bedwars_level = DATA["player"]["achievements"]["bedwars_level"]
try:
    bedwars_wins = DATA["player"]["achievements"]["bedwars_wins"]
except KeyError:
    bedwars_wins = 0
print(f"{answer}'s bedwars level is {bedwars_level} with {bedwars_wins} wins.")
net_exp = DATA["player"]["networkExp"]
net_level = math.floor((((math.sqrt(net_exp + 15312.5)) - (125 / math.sqrt(2))) / 25*math.sqrt(2)) / 2)
print(f"{answer}'s network level is {net_level}")
skywars_exp = DATA["player"]["stats"]["SkyWars"]["skywars_experience"]
skywars_level = math.floor(sw_xp_to_lvl(skywars_exp))
try:
    skywars_wins = 0
    skywars_wins_lab = DATA["player"]["achievements"]["skywars_wins_lab"]
    skywars_wins = skywars_wins + skywars_wins_lab
except KeyError:
    skywars_wins = skywars_wins
try:
    skywars_wins_solo = DATA["player"]["achievements"]["skywars_wins_solo"]
    skywars_wins = skywars_wins + skywars_wins_solo
except KeyError:
    skywars_wins = skywars_wins
try:
    skywars_wins_teams = DATA["player"]["achievements"]["skywars_wins_team"]
    skywars_wins = skywars_wins + skywars_wins_teams
except KeyError:
    skywars_wins = skywars_wins
print(f"{answer}'s skywars level is {skywars_level} with {skywars_wins} wins")


if bedwars_level >= 75 or skywars_level >= 4:
    if net_level >= 25:
        print(f"{answer} is eligible for the main guild.")
    else:
        print(f"{answer} is not eligible for the main guild.")
else:
    print(f"{answer} is not eligible for the main guild.")

