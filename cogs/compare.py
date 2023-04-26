import discord
from discord.ext import commands
import requests

class Compare(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("compare.py is ready")

    @commands.command()
    async def compare(self, ctx, *message):
        listofplayers = []
        for i in range(len(message)):
            player = message[i].replace(",", "")
            listofplayers.append(player)

        listofplayerids = {}
        for p in range(len(listofplayers)):
            playername = listofplayers[p]   
            print(playername)
            playerid = self.getplayerid(playername)
            print(playerid)
            listofplayerids[playerid] = playername
        
        await ctx.send(listofplayerids)
    
    def getplayerid(self, playername):
        response = requests.get('https://tone.sleepycat.date/v2/client/players').json()
        r = response.keys()
        playerid = ""
        for i in r:
            p = response[i]['username']
            if (p.lower() == playername.lower()):
                playerid = i
                break
        return playerid    

async def setup(client):
    await client.add_cog(Compare(client))

    