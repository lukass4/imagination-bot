import discord
from discord.ext import commands
import os
import random
import time
from discord.ext import tasks
import json
import asyncio
import requests
import json
from pprint import pprint
import math
from mojang import MojangAPI

client = commands.Bot(command_prefix = "/")

@client.event
async def on_ready():
    print("Bot is online!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="Hamza Client"))

def is_bot_admin(ctx):
    if ctx.author.id == 562711070242766850 or ctx.author.id == 539029892155572226:
        return

@client.command()
async def verify(ctx, user):
    if not user == None:
       
        uuid = MojangAPI.get_uuid(user)
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
        net_exp = DATA["player"]["networkExp"]
        net_level = math.floor((((math.sqrt(net_exp + 15312.5)) - (125 / math.sqrt(2))) / 25*math.sqrt(2)) / 2)
        await ctx.send(f"{user}'s Network level is {net_level}")
        bedwars_level = DATA["player"]["achievements"]["bedwars_level"]
        try:
            bedwars_wins = DATA["player"]["achievements"]["bedwars_wins"]
        except KeyError:
            bedwars_wins = 0
        await ctx.send(f"{user}'s Bedwars level is {bedwars_level} with {bedwars_wins} wins.")
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
        await ctx.send(f"{user}'s Skywars level is {skywars_level} with {skywars_wins} wins")
        if bedwars_level >= 75 or skywars_level >= 4:
            if net_level >= 25:
                await ctx.send(f"{user} **is** eligible for the main guild.")
            elif user == "hamza_talaat":
                await ctx.send(f"{user} **is not** eligible for the main guild.")
            else:
                await ctx.send(f"{user} **is not** eligible for the main guild.")
        elif net_level >= 100:
            await ctx.send(f"{user} **may be** eligible for the main guild. \n (as their network level is above 100 but they dont meet the SW or BW reqs)")
        else:
            await ctx.send(f"{user} **is not** eligible for the main guild.")

@verify.error
async def verify_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I cant look up stats for noone dumbass")

@client.command()
async def qverify(ctx, user):
    def sw_xp_to_lvl(xp):
        xps = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
        if xp >= 15000:
            return (xp - 15000) / 10000. + 12
        else:
            for i in range(len(xps)):
                if xp < xps[i]:
                    return i + float(xp - xps[i-1]) / (xps[i] - xps[i-1])
    uuid = MojangAPI.get_uuid(user)
    url = f"https://api.hypixel.net/player?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&uuid={uuid}"
    DATA = requests.get(url).json()

    bedwars_level = DATA["player"]["achievements"]["bedwars_level"]
    skywars_exp = DATA["player"]["stats"]["SkyWars"]["skywars_experience"]
    skywars_level = math.floor(sw_xp_to_lvl(skywars_exp))
    net_exp = DATA["player"]["networkExp"]
    net_level = math.floor((((math.sqrt(net_exp + 15312.5)) - (125 / math.sqrt(2))) / 25*math.sqrt(2)) / 2)

    if bedwars_level >= 75 or skywars_level >= 4:
        if net_level >= 25:
            await ctx.send(f"{user} **is** eligible for the main guild.")
        else:
            await ctx.send(f"{user} **is not** eligible for the main guild.")
    elif net_level >= 100:
        await ctx.send(f"{user} **may be** eligible for the main guild. \n (as their network level is above 100 but they dont meet the SW or BW reqs)")
    else:
        await ctx.send(f"{user} **is not** eligible for the main guild.")

@qverify.error
async def qverify_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I cant look up stats for noone dumbass")

@client.command()
async def uuid(ctx, user):
    await ctx.send(f"{user}'s UUID is `{MojangAPI.get_uuid(user)}`")

@uuid.error
async def uuid_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("FOR THE LAST TIME PLEASE SPECIFY A PLAYER FFS!")

@client.command()
async def bedwars(ctx, user):
    uuid = MojangAPI.get_uuid(user)
    url = f"https://api.hypixel.net/player?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&uuid={uuid}"
    DATA = requests.get(url).json()

    bedwars_level = DATA["player"]["achievements"]["bedwars_level"]
    try:
        bedwars_losses = DATA["player"]["stats"]["Bedwars"]["losses_bedwars"]
    except KeyError:
        bedwars_losses = 0
    try:
        bedwars_kills = DATA["player"]["stats"]["Bedwars"]["kills_bedwars"]
    except KeyError:
        bedwars_kills = 0
    try:
        bedwars_deaths = DATA["player"]["stats"]["Bedwars"]["deaths_bedwars"]
    except KeyError:
        bedwars_deaths = 0
    try:
        winstreak = DATA["player"]["stats"]["Bedwars"]["winstreak"]
    except KeyError:
        winstreak = 0
    try:
        final_kills = DATA["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
    except KeyError:
        final_kills = 0
    try:
        bedwars_final_deaths = DATA["player"]["stats"]["Bedwars"]["final_deaths_bedwars"]
    except KeyError:
        bedwars_final_deaths = 0
    try:
        bedwars_deaths = DATA["player"]["stats"]["Bedwars"]["deaths_bedwars"]
    except KeyError:
        bedwars_deaths = 0
    try:
        bedwars_wins = DATA["player"]["stats"]["Bedwars"]["wins_bedwars"]
    except KeyError:
        bedwars_wins = 0
    await ctx.send(f"""{user}'s Bedwars Stats:
Level: `{bedwars_level}`
Wins: `{bedwars_wins}` 
Final Kills: `{final_kills}`
Kills: `{bedwars_kills}`
Winstreak: `{winstreak}`
Losses: `{bedwars_losses}`
Final Deaths: `{bedwars_final_deaths}`
Deaths: `{bedwars_deaths}`
Plancke: <https://plancke.io/hypixel/player/stats/{user}#BedWars>""")
client.run("ODMwMTIwNjc5NDc5MTgxMzEz.YHCEIA.kBkWUQlLUV4kfQ5MVTBkKD7xAag")