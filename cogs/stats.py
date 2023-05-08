from urllib import request
import discord
from discord.ext import commands
import requests

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("stats.py is ready")

    @commands.command(aliases=["compare"])
    async def stats(self, ctx, *message):
        error = False
        players = {}
        servers = []
        server = ""
        weaponid= ""
        weaponname= ""
     
        if(message == ()):
            await ctx.send("```No player given```")
            error = True

        for i in message:
            item = i.replace(",", "")
            function_dict = self.message_handler(item)
            if(function_dict['player'] != None):
                players[item] = self.getplayerid(item)
            if(function_dict['weapon'] != None):
                weaponname = function_dict["weapon"][1]
                weaponid= function_dict['weapon'][0]
            if(function_dict['server'] != None):
                servers.append(function_dict['server']) 

        servers.append(self.getserver("", " ".join(message)))

        if(len(servers) != 0 and len(message) != 1):     
            if(len(message) == 2 and weaponid != ""):
                server = ""
            elif(len(servers) > 1):   
                for i in servers:
                    if(i.lower() in " ".join(message).lower()):
                        server = i
                        break   
            else:
                server = servers[0]

        if(len(players) == 0 and error == False):
            error = True
            await ctx.send("```No existing player found, check if the name is correct or has changed```")

        list_of_stats = []
        for i in players.keys():
            if(i.lower() not in server.lower()):
                stats = self.getstats(playerid=players[i],weaponid=weaponid, weaponname=weaponname, server=server) 
                list_of_stats.append(stats)

        if ("".join(list_of_stats) != ""):
            if(server != ""):
                botmessage = str("Stats for " + server + "\n" + "---------------------" + "\n") 
            else:
                botmessage = str("Stats for all servers\n" + "---------------------" + "\n") 
            divider = str("\n --------------------- \n")
            botmessage = botmessage + divider.join(list_of_stats)
    
        await ctx.send(f'```{botmessage}```')

    def message_handler(self, message):
        player = False
        weapon = False
        server = False
        return_message = {"player": None, "weapon": None, "server": None}

        playerid = self.getplayerid(message)
        if(playerid != ""):
            player = True

        weaponid, weaponname = self.getweaponid(message)
        if(weaponid != ""):
            weapon = True

        servername = self.getserver(message)
        if(servername != ""):
            server = True

        if(server):
            return_message["server"] = servername
        if(player):
            return_message["player"] = playerid
        if(weapon):
            return_message["weapon"] = [weaponid, weaponname]

        return return_message

    def getplayerid(self, playername):
        playerid = ""
        payload = str("username=") + playername
        response = requests.get('https://northstar.tf/accounts/lookup_uid', params=payload).json()
        if (response['matches'] != None):
            playerid = response['matches'][0]
            return str(playerid)

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

    def getserver(self, snippet, fullmessage = ""):
        server = ""
        response = requests.get('https://tone.sleepycat.date/v2/client/servers').json()
        servers = response.keys()

        for i in servers:
            if(snippet.lower() in i.lower()):
                server = i
            if(i.lower() in fullmessage.lower()):
                server = i
                break

        return server

    def getstats(self, playerid, weaponid = "", weaponname = "", server = ""):
        payload = {'player': playerid, 'weapon': weaponid, 'server': server}
        response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
        if(response == {}):
             errorresponse = requests.get("https://northstar.tf/accounts/get_username", params={"uid": playerid}).json()
             if(errorresponse['matches'] != None):
                playername = errorresponse['matches'][0]
                return str("No stats found for player: " + playername)
        
        killstats = response[str(playerid)]

        botmessage = str("Playername: " + killstats['username'] + '\n' + "Kills     : " + str(killstats['kills']) + '\n' )
              
        if(weaponid != ""):
            deaths=killstats['deaths_while_equipped']
            if(deaths == 0):
                deaths = 1;
            botmessage += str(str("Deaths    : " + str(killstats['deaths_while_equipped'])) + '\n' + str("Weapon    : " + weaponname) + '\n' 
                       + str(str("weapon KD : " + str("{:0.2f}".format(killstats['kills']/deaths)))+ '\n' + str("Deaths to : " + str(killstats['deaths']))))
        else:
            deaths=killstats['deaths']
            if(deaths == 0):
                deaths = 1;
            botmessage = botmessage + str("Deaths    : " + str(killstats['deaths'])) + '\n' + str("KD        : " + str("{:0.2f}".format(killstats['kills']/deaths)))

        return botmessage

async def setup(client):
    await client.add_cog(Stats(client))

