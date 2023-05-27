import discord
from discord.ext import commands
from discord import app_commands
import requests

from Reuse.getServer import getserver
from Reuse.getWeapon import getweaponid

class SlashLeaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashLeaderboard.py is ready")

    @app_commands.command(name="leaderboard", description="Gives the leaderboard of selected filter, possible to be narrowed down on weapon and server")
    @app_commands.describe(board = "The filter that decides the stat the leaderboard gets ordered at",weapon = "Ingame Weaponname", servername = "A Tone supported server")
    @app_commands.rename(board = "filter", servername = "server")
    async def leaderboard(self, interaction: discord.Interaction, board: str, weapon : str = "", servername : str = ""):
        boards = ["kd", "avgd", "maxd", "totald","deaths", "kills"]
        server = ""
        weaponid= ""
        weaponname= ""

        if(weapon != ""):
            weaponid, weaponname = getweaponid(weapon)
        if(servername != ""):
            server = getserver(servername)

        if(board in boards):
            botmessage = self.getleaderboard(weaponid=weaponid, weaponname=weaponname, server=server, board=board)
        else:
            botmessage = "You gave a none existing filter"

        await interaction.response.send_message(f'```{botmessage}```')


    def getleaderboard(self, board, weaponid="", weaponname="", server=""):
        easyfilter = False
        hardfilter = False
        payload = {"weapon": weaponid, "server": server}
        response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
        players = response.keys()

        if(board.lower() in ["kills", "deaths", "maxd", "totald"]):
            if(board.lower() == "totald"):
                board = "total_distance"
            if(board.lower() == "maxd"):
                board = "max_distance"       
            easyfilter = True
        else:
            hardfilter = True

        if(len(players) < 10):
            lb_length = len(players)
        else:
            lb_length = 10

        top10 = {}
        while(len(top10)<lb_length):
            current = 0 
            name = ""
            for p in players:
                stats = response[p]
                if(easyfilter):
                    checked = stats[str(board)]
                if(hardfilter):
                    if(board.lower() == "kd"):
                        if(weaponid != ""):
                            deaths = stats['deaths_while_equipped']
                        else:
                            deaths = stats['deaths']
                        if(deaths == 0):
                            deaths = deaths + 1
                        checked = round(stats["kills"] / deaths, 2)
                    if(board.lower() == "avgd"):
                        if(stats["kills"] == 0):
                            kills = 1
                        else:
                            kills = stats["kills"]
                        checked = round(stats["total_distance"] / kills, 2)
                #print(checked, ", ", current )
                if(checked >= current and stats["username"] not in top10.keys()):
                     #print(checked, ", ", current)
                     current = checked
                     name = stats['username']
        
            top10[name] = current

        if(board.lower() == "deaths"):
            inbetween = "to"
        else:
            inbetween = "with"

        if(server == ""):
            server = "all servers"
        if(weaponname == ""):
            weaponname = "any weapon"

        botmessage = str(f"Leaderboard of {board} {inbetween} {weaponname} for {server}\n-------------------------------\n")

        counter = 1
        for i, j in top10.items():
            if(hardfilter):
                stat = str("{:0.2f}".format(j))
            if(easyfilter):
                stat = str(j)
            botmessage = botmessage + str(f"{str(counter):<2}"+ " - " + f"{i :<20}" + " : "+ f"{stat:<8}" + "\n")
            counter= counter+1 

        return botmessage
    
    @leaderboard.autocomplete("weapon")
    async def autocomplete_weapon(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        weaponlist = ['execution', 'car', 'charge rifle', 'double take', 'epg', 'volt', 'lstar', 'r97', 'r-201', 'smart pistol', 'kraber', 'flatline', 're-45 auto', 'alternator', 'frag grenade', 'g2', 'spitfire', 'smr', 'softball', 'firestar', 'melee', 'masstiff', 'mgl', 'r-101', 'wingman', 'invalid', 'thunderbolt', 'dmr', 'electric smoke', 'cold war', 'satchel', 'eva-8 auto', 'mozambique', 'wingman elite', 'gravity star', 'pulse blade', 'archer', 'outOfBounds', 'mind crime', 'devotion', 'fall', 'p2016', 'arc grenade', 'hemlok', 'phase shift']
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
        return data
    
    @leaderboard.autocomplete("board")
    async def autocomplete_server(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        boards = ["kd", "avgd", "maxd", "totald","deaths", "kills"]
        for board_choice in boards:
            if(current.lower() in board_choice.lower()):
                data.append(app_commands.Choice(name=board_choice, value=board_choice))
        return data

async def setup(client):
    await client.add_cog(SlashLeaderboard(client))