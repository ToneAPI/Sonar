import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
import requests
from Reuse.getGamemode import getgamemodeid
from Reuse.getLeaderboard import create_leaderboard_message, getleaderboard
from Reuse.getMap import getmapid

from Reuse.getServer import getserver
from Reuse.getWeapon import getweaponid

class SlashLeaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashLeaderboard.py is ready")

    @app_commands.command(name="leaderboard", description="Gives the leaderboard of selected filter, possible to be narrowed down on weapon and server")
    @app_commands.describe(board = "The filter that decides the stat the leaderboard gets ordered at",weapon = "Ingame Weaponname", servername = "A Tone supported server", givenmap = "Ingame map", givengamemode="ingame gamemode")
    @app_commands.rename(board = "filter", servername = "server", givenmap = "map", givengamemode= "gamemode")
    async def leaderboard(self, interaction: discord.Interaction, board: str, weapon : str = "", servername : str = "", givenmap : str = "", givengamemode : str = ""):
        boards = ["kd", "avgd", "maxd", "totald","deaths", "kills"]
        server = ""
        weaponid = ""
        weaponname = ""
        mapname = ""
        gamemode = ""
        mapid = ""
        gamemodeid = ""

        async with aiohttp.ClientSession() as session:
            if(weapon != ""):
                weaponid, weaponname = getweaponid(weapon)
            if(givengamemode != ""):
                gamemodeid, gamemode = getgamemodeid(givengamemode)
            if(givenmap != ""):
                mapid, mapname = getmapid(givenmap)
            if(servername != ""):
                server = await getserver(session,servername)

            if(board in boards):
                botmessage = create_leaderboard_message(weaponid=weaponid, weaponname=weaponname, server=server, board=board, mapid=mapid, mapname=mapname, gamemode=gamemode, gamemodeid=gamemodeid)
            else:
                botmessage = "You gave a none existing filter"

        await interaction.response.send_message(embed=botmessage)

    
    @leaderboard.autocomplete("weapon")
    async def autocomplete_weapon(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        weaponlist = ['execution', 'car', 'charge rifle', 'double take', 'epg', 'volt', 'lstar', 'r97', 'r-201', 'smart pistol', 'kraber', 'flatline', 're-45 auto', 'alternator', 'frag grenade', 'g2', 'spitfire', 'smr', 'softball', 'firestar', 'melee', 'mastiff', 'mgl', 'r-101', 'wingman', 'invalid', 'thunderbolt', 'dmr', 'electric smoke', 'cold war', 'satchel', 'eva-8 auto', 'mozambique', 'wingman elite', 'gravity star', 'pulse blade', 'archer', 'outOfBounds', 'mind crime', 'devotion', 'fall', 'p2016', 'arc grenade', 'hemlok', 'phase shift', 'double barrel shotgun']
        for weapon_choice in weaponlist:
            if(current.lower() in weapon_choice.lower()):
                data.append(app_commands.Choice(name=weapon_choice, value=weapon_choice))
        return data
    
    @leaderboard.autocomplete("servername")
    async def autocomplete_server(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        servers = requests.get("https://tone.sleepycat.date/v2/client/servers").json()
        for server_choice in servers.keys():
            if(current.lower() in server_choice.lower()):
                data.append(app_commands.Choice(name=server_choice, value=server_choice))
        return data[:25]
    
    @leaderboard.autocomplete("board")
    async def autocomplete_server(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        boards = ["kd", "avgd", "maxd", "totald","deaths", "kills"]
        for board_choice in boards:
            if(current.lower() in board_choice.lower()):
                data.append(app_commands.Choice(name=board_choice, value=board_choice))
        return data[:25]
    
    @leaderboard.autocomplete("givenmap")
    async def autocomplete_map(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        maplist = ['angel city', 'black water canal', 'coliseum', 'pillars', 'colony', 'complex', 'crashsite', 'drydock', 'eden', 'forwardbase kodai', 'glitch', 'boomtown', 'homestead', 'deck', 'meadow', 'stacks', 'township', 'trafic', 'uma', 'relic', 'rise', 'exoplanet', 'wargames']
        for map_choice in maplist:
            if(current.lower() in map_choice.lower()):
                data.append(app_commands.Choice(name=map_choice, value=map_choice))
        return data[:25]

    @leaderboard.autocomplete("givengamemode")
    async def autocomplete_gamemode(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        gamemodelist = ['attrition', 'bounty hunt', 'one in the chamber', 'amped hardpoint', 'capture the flag', 'frontier defense', 'free for all', 'frontier war', 'gungame', 'infection', 'last titan standing', 'marked for death', 'pilots vs. pilots', 'sticks and stones', 'skirmish', 'titan brawl']
        for gamemode_choice in gamemodelist:
            if(current.lower() in gamemode_choice.lower()):
                data.append(app_commands.Choice(name=gamemode_choice, value=gamemode_choice))
        return data[:25]

async def setup(client):
    await client.add_cog(SlashLeaderboard(client))
