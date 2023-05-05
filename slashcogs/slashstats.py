import discord
from discord.ext import commands
from discord import app_commands
import requests

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
        error = False
        playernames = playernames.replace(",", "")
        playernames = playernames.split(" ")
        players = []
        server = ""
        weaponid= ""
        weaponname= ""
     
        print(playernames)

        for i in playernames:
            playerid = self.getplayerid(i)
            if(playerid != ""):
                players.append(playerid)
        if(weapon != ""):
            weaponid, weaponname = self.getweaponid(weapon)
        if(servername != ""):
            server = self.getserver(servername)

        if(len(players) == 0 and error == False):
            error = True
            await interaction.response.send_message("```No existing player found, check if the name is correct or has changed```")

        list_of_stats = []
        for i in players:
            stats = self.getstats(playerid=i,weaponid=weaponid, weaponname=weaponname, server=server) 
            list_of_stats.append(stats)

        if ("".join(list_of_stats) != ""):
            if(server != ""):
                botmessage = str("Stats for " + server + "\n" + "---------------------" + "\n") 
            else:
                botmessage = str("Stats for all servers\n" + "---------------------" + "\n") 
            divider = str("\n --------------------- \n")
            botmessage = botmessage + divider.join(list_of_stats)
    
        await interaction.response.send_message(f'```{botmessage}```')


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
        if(weaponid == ""):
            weaponname = ""

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
            botmessage += str("Deaths    : " + str(killstats['deaths_while_equipped'])) + '\n' + str("Weapon    : " + weaponname) + '\n' + str(str("weapon KD : " + str("{:0.2f}".format(killstats['kills']/deaths))))
        else:
            deaths=killstats['deaths']
            if(deaths == 0):
                deaths = 1;
            botmessage = botmessage + str("Deaths    : " + str(killstats['deaths'])) + '\n' + str("KD        : " + str("{:0.2f}".format(killstats['kills']/deaths)))

        return botmessage
    
    @stats.autocomplete("weapon")
    async def autocomplete_weapon(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        weaponlist = ['execution', 'car', 'charge rifle', 'double take', 'epg', 'volt', 'lstar', 'r97', 'r-201', 'smart pistol', 'kraber', 'flatline', 're-45 auto', 'alternator', 'frag grenade', 'g2', 'spitfire', 'smr', 'softball', 'firestar', 'melee', 'masstiff', 'mgl', 'r-101', 'wingman', 'invalid', 'thunderbolt', 'dmr', 'electric smoke', 'cold war', 'satchel', 'eva-8 auto', 'mozambique', 'wingman elite', 'gravity star', 'pulse blade', 'archer', 'outOfBounds', 'mind crime', 'devotion', 'fall', 'p2016', 'arc grenade', 'hemlok', 'phase shift']
        for weapon_choice in weaponlist:
            if(current.lower() in weapon_choice.lower()):
                data.append(app_commands.Choice(name=weapon_choice, value=weapon_choice))
        return data
    
    @stats.autocomplete("servername")
    async def autocomplete_server(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        data = []
        servers = requests.get("https://tone.sleepycat.date/v2/client/servers").json()
        for server_choice in servers.keys():
            if(current.lower() in server_choice.lower()):
                data.append(app_commands.Choice(name=server_choice, value=server_choice))
        return data
        

async def setup(client):
    await client.add_cog(SlashStats(client))

