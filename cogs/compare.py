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
        playerid = ""
        payload = str("username=") + playername
        response = requests.get('https://northstar.tf/accounts/lookup_uid', params=payload).json()
        playerid = response['matches'][0]
        return str(playerid)

async def setup(client):
    await client.add_cog(Compare(client))

    