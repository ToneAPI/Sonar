import asyncio
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
import requests
from Reuse.getGamemode import getgamemodeid
from Reuse.getMap import getmapid

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
    @app_commands.describe(playernames = "Ingame name of the player or players", weapon = "Ingame Weaponname", servername = "A Tone supported server", givenmap = "Ingame map", givengamemode="ingame gamemode")
    @app_commands.rename(playernames = "player", servername = "server", givenmap = "map", givengamemode= "gamemode")
    async def stats(self, interaction: discord.Interaction, playernames : str, weapon : str = "", servername : str = "", givenmap : str = "", givengamemode : str = ""):
        server = ""
        weaponid = ""
        weaponname = ""
        mapname = ""
        gamemode = ""
        mapid = ""
        gamemodeid = ""

        playernames = playernames.replace(",", " ")
        playernames = playernames.split(" ")

        async with aiohttp.ClientSession() as session:
            players = await get_all_playerids(session, playernames)
            players = players[0]
            if(players == {} or players.keys() == []):
                await interaction.response.send_message("```No existing player given.\nIf you put in multiple players make sure to split them with a comma(,)```")
                return

            if(weapon != ""):
                weaponid, weaponname = getweaponid(weapon)
            if(givengamemode != ""):
                gamemodeid, gamemode = getgamemodeid(givengamemode)
            if(givenmap != ""):
                mapid, mapname = getmapid(givenmap)
            if(servername != ""):
                server = await getserver(session, servername)

        async with aiohttp.ClientSession() as session:
            botmessage, img_file = await get_allplayer_stats(session, players.values(), weaponid, weaponname, server, mapid, mapname, gamemodeid, gamemode)


        if(img_file != ""):
            await interaction.response.send_message(file=img_file, embed=botmessage)
        else:
            await interaction.response.send_message(embed=botmessage)


    @stats.autocomplete("playernames")
    async def autocomplete_player(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        async with aiohttp.ClientSession() as session:
            async with session.get(os.environ.get("TONE_ENDPOINT") + '/v2/client/players') as r:
                players = await r.json()

        for player_choice in players.keys():
            try:
                if(current.lower() in players[player_choice]['username'].lower()):
                    data.append(app_commands.Choice(name=players[player_choice]['username'], value=players[player_choice]['username']))
            except AttributeError:
                pass
        return data[:25]

    @stats.autocomplete("weapon")
    async def autocomplete_weapon(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        weaponlist = ['execution', 'car', 'charge rifle', 'double take', 'epg', 'volt', 'lstar', 'r97', 'r-201', 'smart pistol', 'kraber', 'flatline', 're-45 auto', 'alternator', 'frag grenade', 'g2', 'spitfire', 'smr', 'softball', 'firestar', 'melee', 'mastiff', 'mgl', 'r-101', 'wingman', 'invalid', 'thunderbolt', 'dmr', 'electric smoke', 'cold war', 'satchel', 'eva-8 auto', 'mozambique', 'wingman elite', 'gravity star', 'pulse blade', 'archer', 'outOfBounds', 'mind crime', 'devotion', 'fall', 'p2016', 'arc grenade', 'hemlok', 'phase shift', 'double barrel shotgun']
        for weapon_choice in weaponlist:
            if(current.lower() in weapon_choice.lower()):
                data.append(app_commands.Choice(name=weapon_choice, value=weapon_choice))
        return data[:25]
    
    @stats.autocomplete("servername")
    async def autocomplete_server(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        async with aiohttp.ClientSession() as session:
            async with session.get(os.environ.get("TONE_ENDPOINT") + '/v2/client/servers') as r:
                servers = await r.json()

        for server_choice in servers.keys():
            if(current.lower() in server_choice.lower()):
                data.append(app_commands.Choice(name=server_choice, value=server_choice))
        return data[:25]
    
    @stats.autocomplete("givenmap")
    async def autocomplete_map(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        maplist = ['angel city', 'black water canal', 'coliseum', 'pillars', 'colony', 'complex', 'crashsite', 'drydock', 'eden', 'forwardbase kodai', 'glitch', 'boomtown', 'homestead', 'deck', 'meadow', 'stacks', 'township', 'trafic', 'uma', 'relic', 'rise', 'exoplanet', 'wargames']
        for map_choice in maplist:
            if(current.lower() in map_choice.lower()):
                data.append(app_commands.Choice(name=map_choice, value=map_choice))
        return data[:25]

    @stats.autocomplete("givengamemode")
    async def autocomplete_gamemode(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        gamemodelist = ['attrition', 'bounty hunt', 'one in the chamber', 'amped hardpoint', 'capture the flag', 'frontier defense', 'free for all', 'frontier war', 'gungame', 'infection', 'last titan standing', 'marked for death', 'pilots vs. pilots', 'sticks and stones', 'skirmish', 'titan brawl']
        for gamemode_choice in gamemodelist:
            if(current.lower() in gamemode_choice.lower()):
                data.append(app_commands.Choice(name=gamemode_choice, value=gamemode_choice))
        return data[:25]


async def setup(client):
    await client.add_cog(SlashStats(client))

