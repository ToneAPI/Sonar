import asyncio
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
import requests

from Reuse.getPlayer import get_all_playerids
from Reuse.getServer import getserver
from Reuse.getStats import get_allplayer_stats
from Reuse.getWeapon import getweaponid

class SlashStats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashStats.py is ready")

    @app_commands.command(name="stats", description="Gives the stats of the selected player/players filtered by weapon and server, if given")
    @app_commands.describe(playernames = "Ingame name of the player or players", weapon = "Ingame Weaponname", servername = "A Tone supported server")
    @app_commands.rename(playernames = "player", servername = "server")
    async def stats(self, interaction: discord.Interaction, playernames : str, weapon : str = "", servername : str = ""):
        server = ""
        weaponid = ""
        weaponname = ""

        playernames = playernames.replace(",", " ")
        playernames = playernames.split(" ")

        async with aiohttp.ClientSession() as session:
            players = await get_all_playerids(session, playernames)
            if(players == {} or players.keys() == []):
                await interaction.response.send_message("```No existing player given.\nIf you put in multiple players make sure to split them with a comma(,)```")
                return

            if(weapon != ""):
                weaponid, weaponname = getweaponid(weapon)
            if(servername != ""):
                server = await getserver(session, servername)

        async with aiohttp.ClientSession() as session:
            botmessage = await get_allplayer_stats(session, players.values(), weaponid, weaponname, server)

        await interaction.response.send_message(embed=botmessage)
    
    @stats.autocomplete("weapon")
    async def autocomplete_weapon(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        weaponlist = ['execution', 'car', 'charge rifle', 'double take', 'epg', 'volt', 'lstar', 'r97', 'r-201', 'smart pistol', 'kraber', 'flatline', 're-45 auto', 'alternator', 'frag grenade', 'g2', 'spitfire', 'smr', 'softball', 'firestar', 'melee', 'mastiff', 'mgl', 'r-101', 'wingman', 'invalid', 'thunderbolt', 'dmr', 'electric smoke', 'cold war', 'satchel', 'eva-8 auto', 'mozambique', 'wingman elite', 'gravity star', 'pulse blade', 'archer', 'outOfBounds', 'mind crime', 'devotion', 'fall', 'p2016', 'arc grenade', 'hemlok', 'phase shift']
        for weapon_choice in weaponlist:
            if(current.lower() in weapon_choice.lower()):
                data.append(app_commands.Choice(name=weapon_choice, value=weapon_choice))
        return data
    
    @stats.autocomplete("servername")
    async def autocomplete_server(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        async with aiohttp.ClientSession() as session:
            async with session.get('https://tone.sleepycat.date/v2/client/servers') as r:
                servers = await r.json()

        for server_choice in servers.keys():
            if(current.lower() in server_choice.lower()):
                data.append(app_commands.Choice(name=server_choice, value=server_choice))
        return data
    

async def setup(client):
    await client.add_cog(SlashStats(client))

