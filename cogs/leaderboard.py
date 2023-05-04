import discord
from discord.ext import commands
import requests

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
        servers = []
        server = ""
        weaponid= ""
        weaponname= ""

        if(message == ()):
            error = True
            botmessage = "No leaderboard option selected, choose from:\n"
            for i in boards:
                botmessage = botmessage + i + "\n"
            await ctx.send(botmessage)

        for i in message:
            item = i.replace(",", "")
            if(item.lower() not in boards):
                function_dict = self.message_handler(item)
                if(function_dict['weapon'] != None):
                    weaponname = function_dict["weapon"][1]
                    weaponid= function_dict['weapon'][0]
                if(function_dict['server'] != None):
                    servers.append(function_dict['server'])
            else:
                board = item 

        if(board == "" and error == False):
            error = True
            botmessage = "No leaderboard option selected, choose from:\n"
            for i in boards:
                botmessage = botmessage + i + "\n"
            await ctx.send(botmessage)

        if(len(servers) != 0):           
            if(len(servers) > 1):   
                for i in servers:
                    if(i in " ".join(message)):
                        server = i
                        break   
            else:
                server = servers[0]

        botmessage = self.getleaderboard(weaponid=weaponid, weaponname=weaponname, server=server, board=board)

        await ctx.send(f'```{botmessage}```')

    def message_handler(self, message):
        weapon = False
        server = False
        return_message = {"weapon": None, "server": None}

        weaponid, weaponname = self.getweaponid(message)
        if(weaponid != ""):
            weapon = True

        servername = self.getserver(message)
        if(servername != ""):
            server = True

        if(server):
            return_message["server"] = servername
        if(weapon):
            return_message["weapon"] = [weaponid, weaponname]

        return return_message

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
            botmessage = botmessage + str(str(counter)+ " - " + i + " : "+ stat + "\n")
            counter= counter+1 

        return botmessage

async def setup(client):
    await client.add_cog(Leaderboard(client))