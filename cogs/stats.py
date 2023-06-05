import aiohttp
from discord.ext import commands
from Reuse.getPlayer import get_all_playerids
from Reuse.getServer import getserver
from Reuse.getStats import get_allplayer_stats
from Reuse.getWeapon import getweaponid

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("stats.py is ready")

    @commands.command(aliases=["compare"])
    async def stats(self, ctx, *message):
        error = False
        server = ""
        weaponid = ""
        weaponname = ""

        if(message == ()):
            error = True
            await ctx.send("```No player given```")
            return
        
        message = list(message)
        message = "".join(message)
        message = message.split(",")

        async with aiohttp.ClientSession() as session:
            players, residue = await get_all_playerids(session, message)

            for item in residue:
                if(weaponid == "" and item != None and item != ""):
                    weaponid, weaponname = getweaponid(item)
                if(server == "" and item != None and item != "" and item != weaponname):
                    server = await getserver(session, item)
            

        if(len(players.values()) == 0 and error == False):
            error = True
            await ctx.send("```No existing player found, check if the name is correct or has changed\n\n*Note you need to split filters with a comma```")
            return

        async with aiohttp.ClientSession() as session:
            print(players.values())
            botmessage, img_file = await get_allplayer_stats(session, players.values(), weaponid, weaponname, server)

        if(img_file != ""):
            await ctx.send(file=img_file, embed=botmessage)
        else:
            await ctx.send(embed=botmessage)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        print(err)

async def setup(client):
    await client.add_cog(Stats(client))

