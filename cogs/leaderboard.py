import aiohttp
import discord
from discord.ext import commands
import requests
from Reuse.getLeaderboard import getleaderboard
from Reuse.getServer import getserver

from Reuse.getWeapon import getweaponid

class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leaderboard.py is ready")

    @commands.command(aliases = ["lb", "board", "ranking", "rank"])
    async def leaderboard(self, ctx, *message):
        boards = ["kd", "avgd", "maxd", "totald","deaths", "kills"]
        error = False
        board = ""
        server = ""
        weaponid= ""
        weaponname= ""
        if(message == ()):
            error = True
            botmessage = "No leaderboard option selected, choose from:\n"
            for i in boards:
                botmessage = botmessage + i + "\n"
            await ctx.send(f"```{botmessage}```")

        message = list(message)
        message = "".join(message)
        message = message.split(",")
        async with aiohttp.ClientSession() as session:
            for item in message:
                if(item.lower() in boards):
                    board = item;
                else:
                    if(item != None and item != "" and weaponid == ""):
                        weaponid, weaponname = getweaponid(item)
                    if(item != None and item != ""  and server == "" and item != weaponname):
                        server = await getserver(session, item)


        if(board == "" and error == False):
            error = True
            botmessage = "No leaderboard option selected, choose from:\n"
            for i in boards:
                botmessage = botmessage + i + "\n"

            botmessage = botmessage + "\n*Note you need to split filters with comma's(,)"
            await ctx.send(f"```{botmessage}```")


        botmessage = getleaderboard(weaponid=weaponid, weaponname=weaponname, server=server, board=board)

        await ctx.send(embed=botmessage)


async def setup(client):
    await client.add_cog(Leaderboard(client))