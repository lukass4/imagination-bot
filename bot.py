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
import math
from mojang import MojangAPI
from datetime import datetime

PREFIX = "/"
BOT_TOKEN = "ODMwMTIwNjc5NDc5MTgxMzEz.YHCEIA.kBkWUQlLUV4kfQ5MVTBkKD7xAag"

intents = discord.Intents(messages=True, guilds=True)
intents.members = True

client = commands.Bot(command_prefix = PREFIX, intents=intents)

LJ = client.get_user(562711070242766850)

@client.event
async def on_ready():
    print("Bot is online!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="Bedwar"))
    if BOT_TOKEN == "ODMxMjIwMDMxMzU3NTgzNDUw.YHSD-g.Mk9aO6IxED6psL9tEuAfPFpCDA0":
        return
    elif BOT_TOKEN == "ODMwMTIwNjc5NDc5MTgxMzEz.YHCEIA.kBkWUQlLUV4kfQ5MVTBkKD7xAag":
        LJ = client.get_user(562711070242766850)
        await LJ.send("The main bot has been started.") 

def is_bot_admin(ctx):
    if ctx.author.id == 562711070242766850 or ctx.author.id == 539029892155572226:
        return

def is_lj(ctx):
    if ctx.author.id == 562711070242766850:
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
        bedwars_level = DATA["player"]["achievements"]["bedwars_level"]
        try:
            bedwars_wins = DATA["player"]["achievements"]["bedwars_wins"]
        except KeyError:
            bedwars_wins = 0
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
        if bedwars_level >= 100 or skywars_level >= 5:
            if net_level >= 50:
                eligible = "yes"
            else:
                eligible = "no"
        elif net_level >= 100:
            eligible = "maybe"
        else:
            eligible = "no"
        
        if eligible == "yes":
            embedVar = discord.Embed(title=f"{user} Stats", description=f"Here are the stats for {user}", color=0x2fd668)
            embedVar.add_field(name="Network", value=f"{user}'s Network level is {net_level}", inline=False)
            embedVar.add_field(name="Bedwars", value=f"{user}'s Bedwars level is {bedwars_level} with {bedwars_wins} wins.", inline=False)
            embedVar.add_field(name="Skywars", value=f"{user}'s Skywars level is {skywars_level} with {skywars_wins} wins", inline=False)
            embedVar.add_field(name="Eligible", value=f"{user} **is** eligible for the main guild.", inline=False)
            await ctx.send(embed=embedVar)
        elif eligible == "no":
            embedVar = discord.Embed(title=f"{user} Stats", description=f"Here are the stats for {user}", color=0x2fd668)
            embedVar.add_field(name="Network", value=f"{user}'s Network level is {net_level}", inline=False)
            embedVar.add_field(name="Bedwars", value=f"{user}'s Bedwars level is {bedwars_level} with {bedwars_wins} wins.", inline=False)
            embedVar.add_field(name="Skywars", value=f"{user}'s Skywars level is {skywars_level} with {skywars_wins} wins", inline=False)
            embedVar.add_field(name="Eligible", value=f"{user} **is not** eligible for the main guild.", inline=False)
            await ctx.send(embed=embedVar)
        elif eligible == "maybe":
            embedVar = discord.Embed(title=f"{user} Stats", description=f"Here are the stats for {user}", color=0x2fd668)
            embedVar.add_field(name="Network", value=f"{user}'s Network level is {net_level}", inline=False)
            embedVar.add_field(name="Bedwars", value=f"{user}'s Bedwars level is {bedwars_level} with {bedwars_wins} wins.", inline=False)
            embedVar.add_field(name="Skywars", value=f"{user}'s Skywars level is {skywars_level} with {skywars_wins} wins", inline=False)
            embedVar.add_field(name="Eligible", value=f"{user} **may be** eligible for the main guild.", inline=False)
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed(title=f"{user} Stats", description=f"Here are the stats for {user}", color=0x2fd668)
            embedVar.add_field(name="Network", value=f"{user}'s Network level is {net_level}", inline=False)
            embedVar.add_field(name="Bedwars", value=f"{user}'s Bedwars level is {bedwars_level} with {bedwars_wins} wins.", inline=False)
            embedVar.add_field(name="Skywars", value=f"{user}'s Skywars level is {skywars_level} with {skywars_wins} wins", inline=False)
            embedVar.add_field(name="Eligible", value=f"{user} **is not** eligible for the main guild.", inline=False)

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

    if bedwars_level >= 100 or skywars_level >= 5:
        if net_level >= 50:
            embedVar = discord.Embed(title=f"{user} **is** eligible for the main guild.", description=f"{user} **is** eligible for the main guild.", color=0x2fd668)
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed(title=f"Is {user} eligible?", description=f"{user} **is not** eligible for the main guild.", color=0x2fd668)
            await ctx.send(embed=embedVar)
    elif net_level >= 100:
        embedVar = discord.Embed(title=f"Is {user} eligible?", description=f"{user} **may be** eligible for the main guild. \n (as their network level is above 100 but they dont meet the SW or BW reqs)", color=0x2fd668)
        await ctx.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title=f"Is {user} eligible?", description=f"{user} **is not** eligible for the main guild.", color=0x2fd668)
        await ctx.send(embed=embedVar)

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

@client.command(aliases=["bw", "bwstats", "bedwarsstats"])
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
        bedwars_wins = DATA["player"]["stats"]["Bedwars"]["wins_bedwars"]
    except KeyError:
        bedwars_wins = 0
    embedVar = discord.Embed(title=f"{user}'s bedwars stats", description=f"This is {user}'s bedwars stats", color=0x2fd668)    
    embedVar.add_field(name="Level", value=f"{bedwars_level}", inline=False)
    embedVar.add_field(name="Wins", value=f"{bedwars_wins}", inline=False)
    embedVar.add_field(name="Final Kills", value=f"{final_kills}", inline=False)
    embedVar.add_field(name="Kills", value=f"{bedwars_kills}", inline=False)
    embedVar.add_field(name="Winstreak", value=f"{winstreak}", inline=False)
    embedVar.add_field(name="Losses", value=f"{bedwars_losses}", inline=False)
    embedVar.add_field(name="Final Deaths", value=f"{bedwars_final_deaths}", inline=False)
    embedVar.add_field(name="Deaths", value=f"{bedwars_deaths}", inline=False)
    embedVar.add_field(name="Plancke", value=f"<https://plancke.io/hypixel/player/stats/{user}#BedWars>", inline=False)
    await ctx.send(embed=embedVar)

@bedwars.error
async def bedwars_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("SPECIFY A **PLAYER** :angry:")

@client.command(aliases=["g", "getguild"])
async def guild(ctx, user):
    uuid = MojangAPI.get_uuid(user)
    url = f"https://api.hypixel.net/findGuild?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&byUuid={uuid}"
    DATA = requests.get(url).json()
    if DATA["guild"] == None:
        embedVar = discord.Embed(title=f"{user}'s Guild", description=f"{user} is not in a guild.", color=0x2fd668)
        await ctx.send(embed=embedVar)
    else:
        guild_id = DATA["guild"]
        url = f"https://api.hypixel.net/guild?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&id={guild_id}"
        GUILD_DATA = requests.get(url).json()
        guild_name = GUILD_DATA["guild"]["name"]
        embedVar = discord.Embed(title=f"{user}'s Guild", description=f"{user} is in the guild `{guild_name}`", color=0x2fd668)
        await ctx.send(embed=embedVar)

@guild.error
async def guild_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify a player or I will chop your arms off.")

@client.command(aliases=["gs", "gstats"])
async def guildstats(ctx, user="hamza_talaat"):
    uuid = MojangAPI.get_uuid(user)
    url = f"https://api.hypixel.net/findGuild?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&byUuid={uuid}"
    DATA = requests.get(url).json()
    if DATA["guild"] == None:
        await ctx.send(f"{user} is not in a guild.")
    else:
        guild_id = DATA["guild"]
        url = f"https://api.hypixel.net/guild?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&id={guild_id}"
        GUILD_DATA = requests.get(url).json()
        guild_name = GUILD_DATA["guild"]["name"]
        guild_creation_date = datetime.fromtimestamp(GUILD_DATA["guild"]["created"] / 1000).strftime("%d-%m-%Y (DD-MM-YY)")
        guild_members = 0
        for x in GUILD_DATA["guild"]["members"]:
            guild_members = guild_members + 1
            if x["uuid"] == uuid:
                try:
                    todays_gexp = x["expHistory"][0]
                except KeyError:
                    todays_gexp = 0
                try:
                    joindate = datetime.fromtimestamp(x["joined"] / 1000).strftime("%d-%m-%Y (DD-MM-YY)")
                except KeyError:
                    joindate = "Unknown?"

        embedVar = discord.Embed(title=f"{guild_name}", description=f"Here are stats for {guild_name}", color=0x2fd668)
        embedVar.add_field(name=f"Guild Members", value=f"{str(guild_members)}", inline=False)
        embedVar.add_field(name=f"Guild Creation Date", value=f"The guild was created on {guild_creation_date}", inline=False)
        embedVar.add_field(name=f"Users GEXP", value=f"{user} earned {todays_gexp}GEXP today", inline=False)
        embedVar.add_field(name=f"Users Join-Date", value=f"{user} joined the guild at {joindate}", inline=False)
        embedVar.add_field(name=f"Other Stats coming soon!", value=f"pog championg", inline=False)
        await ctx.send(embed=embedVar)
    
@client.command()
@commands.has_permissions(administrator = True)
async def checkall(ctx):
    url = "https://api.hypixel.net/guild?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&id=5ea44d808ea8c9ab72c4d7cd"
    GUILD_DATA = requests.get(url).json()
    await ctx.send("This may take a while. Please be patient!")
    for user in GUILD_DATA["guild"]["members"]:
        uuid = user["uuid"]
        new_url = f"https://api.hypixel.net/player?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&uuid={uuid}"
        print(f"DEBUG: {new_url}")
        DATA = requests.get(new_url).json()
        def sw_xp_to_lvl(xp):
            xps = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
            if xp >= 15000:
                return (xp - 15000) / 10000. + 12
            else:
                for i in range(len(xps)):
                    if xp < xps[i]:
                        return i + float(xp - xps[i-1]) / (xps[i] - xps[i-1])
        print("DEBUG: " + DATA["player"]["displayname"])
        bedwars_level = DATA["player"]["achievements"]["bedwars_level"]
        skywars_exp = DATA["player"]["stats"]["SkyWars"]["skywars_experience"]
        skywars_level = math.floor(sw_xp_to_lvl(skywars_exp))
        print("DEBUG: " + str(skywars_level))
        net_exp = DATA["player"]["networkExp"]
        net_level = math.floor((((math.sqrt(net_exp + 15312.5)) - (125 / math.sqrt(2))) / 25*math.sqrt(2)) / 2)
        print("DEBUG: " + str(net_level))
        if bedwars_level >= 100 or skywars_level >= 5:
            if net_level >= 50:
                print("DEGUG: second check complete")
            else:
                channel = client.get_channel(832958220850036797)
                await channel.send(DATA["player"]["displayname"])
                
        elif net_level >= 100:
           print("no") 
        else:
            channel = client.get_channel(832958220850036797)
            await channel.send(DATA["player"]["displayname"])
            
        print("DEBUG: a player has been checked!")
    await ctx.send("The check has finished!")

@client.command()
@commands.has_permissions(administrator = True)
async def apiurl(ctx):
    LJ = client.get_user(562711070242766850)
    await LJ.send("Format: `https://api.hypixel.net/player?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&uuid={uuid}`\nYour Stats: `https://api.hypixel.net/player?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&uuid=cf4b41ab702a4bd7bce53ec6cc25d5ca`\nGuild Query: `https://api.hypixel.net/findGuild?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&byUuid=cf4b41ab702a4bd7bce53ec6cc25d5ca`\nGuild Stats: `https://api.hypixel.net/guild?key=924fecf1-37f2-421a-ae07-7f3ca74d9790&id=5ea44d808ea8c9ab72c4d7cd`")



client.run(BOT_TOKEN)

