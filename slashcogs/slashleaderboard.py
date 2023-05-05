import discord
from discord.ext import commands
from discord import app_commands
import requests

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
            weaponid, weaponname = self.getweaponid(weapon)
        if(servername != ""):
            server = self.getserver(servername)

        if(board in boards):
            botmessage = self.getleaderboard(weaponid=weaponid, weaponname=weaponname, server=server, board=board)
        else:
            botmessage = "You gave a none existing filter"

        await interaction.response.send_message(f'```{botmessage}```')

    def getweaponid(self, weaponname):
        weapons ={
                    "execution": "human_execution", 
                    "car": "mp_weapon_car",
                    "charge rifle": "mp_weapon_defender",
                    "double take": "mp_weapon_doubletake",
                    "epg": "mp_weapon_epg",
                    "volt": "mp_weapon_hemlok_smg",
                    "lstar": "mp_weapon_lstar",
                    "r97": "mp_weapon_r97",
                    "r-201": "mp_weapon_rspn101",
                    "smart pistol": "mp_weapon_smart_pistol",
                    "kraber": "mp_weapon_sniper",
                    "flatline": "mp_weapon_vinson",
                    "re-45 auto": "mp_weapon_autopistol",
                    "alternator": "mp_weapon_alternator_smg",
                    "frag grenade": "mp_weapon_frag_grenade",
                    "g2": "mp_weapon_g2",
                    "spitfire": "mp_weapon_lmg",
                    "smr": "mp_weapon_smr",
                    "softball": "mp_weapon_softball",
                    "firestar": "mp_weapon_thermite_grenade",
                    "melee": "melee_pilot_emptyhanded",
                    "masstiff": "mp_weapon_mastiff",
                    "mgl": "mp_weapon_mgl",
                    "r-101": "mp_weapon_rspn101_og",
                    "wingman": "mp_weapon_wingman",
                    "invalid": "invalid",
                    "thunderbolt": "mp_weapon_arc_launcher",
                    "dmr": "mp_weapon_dmr",
                    "electric smoke": "mp_weapon_grenade_electric_smoke",
                    "cold war": "mp_weapon_pulse_lmg",
                    "satchel": "mp_weapon_satchel",
                    "eva-8 auto": "mp_weapon_shotgun",
                    "mozambique": "mp_weapon_shotgun_pistol",
                    "wingman elite": "mp_weapon_wingman_n",
                    "gravity star": "mp_weapon_grenade_gravity",
                    "pulse blade": "mp_weapon_grenade_sonar",
                    "archer": "mp_weapon_rocket_launcher",
                    "outOfBounds": "outOfBounds",
                    "mind crime": "mind_crime",
                    "devotion": "mp_weapon_esaw",
                    "fall": "fall",
                    "p2016": "mp_weapon_semipistol",
                    "arc grenade": "mp_weapon_grenade_emp",
                    "hemlok": "mp_weapon_hemlok",
                    "phase shift": "phase_shift"
                }
    
        weaponid = ""
        for weapon in weapons:     
            if(weaponname.lower() in weapon.lower()):     
                weaponid = weapons[weapon]
                weaponname = weapon
                break

        return weaponid, weaponname

    def getserver(self, snippet):
        server = ""
        response = requests.get('https://tone.sleepycat.date/v2/client/servers').json()
        servers = response.keys()

        for i in servers:
            if(snippet.lower() in i.lower()):
                server = i
                break

        return server
    
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

        top10 = {}
        while(len(top10)<10):
            current = 0 
            name = ""
            for p in players:
                stats = response[p]
                if(easyfilter):
                    checked = stats[str(board)]
                if(hardfilter):
                    if(board.lower() == "kd"):
                        if (stats['deaths'] == 0):
                            deaths = 1
                        else:
                            deaths = stats['deaths']
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
            botmessage = botmessage + str(f"{str(counter):<2}"+ " - " + f"{i :<15}" + " : "+ f"{stat:<8}" + "\n")
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