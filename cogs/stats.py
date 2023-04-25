from urllib import request
import discord
from discord.ext import commands
import requests

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("stats.py is ready")

    @commands.command()
    async def stats(self, ctx, pmessage="any player", message2="any weapon"):
        message = pmessage
        print(message)
        print(message2)
        if(message != "any player"):
            if(message2 != "any weapon"):
                message = message[:-1]
            response = requests.get('https://tone.sleepycat.date/v2/client/players').json()
            r = response.keys()
            playerid = ""
            for i in r:
                p = response[i]['username']
                if (p == message):
                    playerid = i
                    break
            
            if (playerid != ""):
                killstats = response[playerid]
                botmessage = str(
                    "Playername: " + killstats['username'] + '\n' +
                    "Kills: " + str(killstats['kills']) + '\n' +
                    "Deaths " + str(killstats['deaths']) + '\n' +
                    "KD: " + str("{:0.2f}".format(killstats['kills']/killstats['deaths']))
                    )
            else:
                botmessage = "This player doesnt exist"
        else:
            botmessage = "No name given"
        await ctx.send(botmessage)


async def setup(client):
    await client.add_cog(Stats(client))