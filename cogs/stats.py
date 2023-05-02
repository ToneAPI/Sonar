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

    @commands.command()
    async def stats(self, ctx, message="any player", message2="any weapon", *message3):  
        if(message != "any player"):
            weaponid = ""

            if(message3 != ()):
                server = self.getserver(" ".join(message3))
                servermessage = server
            else: 
                server = ""
                servermessage = "all servers"
                
            if(message2 != "any weapon"):
                message = message[:-1]
                weaponid = self.getweaponid(message2)
            playerid = ""
            playerid = self.getplayerid(message);
            if (playerid != ""):
                payload = {'player': playerid, 'weapon': weaponid, 'server': server}
                response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
                killstats = response[playerid]

                botmessage = str("Stats for " + servermessage + "\n" + "---------------------" + "\n") + str("Playername: " + killstats['username'] + '\n' + "Kills     : " + str(killstats['kills']) + '\n' )
                
                if(weaponid != ""):
                    deaths=killstats['deaths_while_equipped']
                    if(deaths == 0):
                        deaths = 1;
                    botmessage += str("Deaths    : " + str(killstats['deaths_while_equipped'])) + '\n' + str("Weapon    : " + message2) + '\n' + str(str("weapon KD : " + str("{:0.2f}".format(killstats['kills']/deaths))))
                else:
                    deaths=killstats['deaths']
                    if(deaths == 0):
                        deaths = 1;
                    botmessage = botmessage + str("Deaths    : " + str(killstats['deaths'])) + '\n' + str("KD        : " + str("{:0.2f}".format(killstats['kills']/deaths)))
            else:
                botmessage = "This player doesnt exist"
        else:
            botmessage = "No name given"

        await ctx.send(f'```{botmessage}```')

    def getplayerid(self, playername):
        playerid = ""
        payload = str("username=") + playername
        response = requests.get('https://northstar.tf/accounts/lookup_uid', params=payload).json()
        if (response['matches'] != None):
            playerid = response['matches'][0]
        return str(playerid)

    def getweaponid(self, weaponname):
        response = requests.get('https://tone.sleepycat.date/v2/client/weapons').json()
        r = response.keys()
        
        weapon_dict = {'execution': 'human_execution',
                    'mp_weapon_car': 'car',
                    'mp_weapon_defender': 'charge_rifle',
                    'mp_weapon_doubletake': 'double_take',
                    'mp_weapon_epg': 'epg',
                    'mp_weapon_hemlok_smg': 'volt',
                    'mp_weapon_lstar': 'lstar',
                    'mp_weapon_r97':'r97',
                    'mp_weapon_rspn101': 'r-201',
                    'mp_weapon_smart_pistol': 'smart_pistol',
                    'mp_weapon_sniper': 'kraber',
                    'mp_weapon_vinson': 'flatline',
                    'mp_weapon_autopistol': 're-45_auto',
                    'mp_weapon_alternator_smg': 'alternator',
                    'mp_weapon_frag_grenade': 'frag_grenade',
                    'mp_weapon_g2': 'g2',
                    'mp_weapon_lmg': 'spitfire',
                    'mp_weapon_smr': 'smr',
                    'mp_weapon_softball': 'softball',
                    'mp_weapon_thermite_grenade': 'firestar',
                    'pilot_emptyhanded': 'melee',
                    'mp_weapon_mastiff': 'masstiff',
                    'mp_weapon_mgl': 'mgl',
                    'mp_weapon_rspn101_og': 'r-101',
                    'mp_weapon_wingman': 'wingman',
                    'invalid': 'invalid',
                    'mp_weapon_arc_launcher': 'thunderbolt',
                    'mp_weapon_dmr': 'dmr',
                    'mp_weapon_grenade_electric_smoke': 'electric_smoke',
                    'mp_weapon_pulse_lmg': 'cold_war',
                    'mp_weapon_satchel': 'satchel',
                    'mp_weapon_shotgun': 'eva-8_auto',
                    'mp_weapon_shotgun_pistol': 'mozambique', 
                    'mp_weapon_wingman_n': 'wingman_elite',
                    'mp_weapon_grenade_gravity': 'gravity_star',
                    'mp_weapon_grenade_sonar': 'pulse_blade',
                    'mp_weapon_rocket_launcher': 'archer',
                    'outOfBounds': 'outOfBounds',
                    'mind_crime': 'mind_crime',
                    'mp_weapon_esaw': 'devotion',
                    'fall': 'fall',
                    'mp_weapon_semipistol': 'p2016',
                    'mp_weapon_grenade_emp': 'arc_grenade',
                    'mp_weapon_hemlok': 'hemlok',
                    'melee_pilot_emptyhanded': 'melee',
                    'phase_shift': 'phase_shift'
                    }
        weaponid = ""
        for i in r:
            if(i in weapon_dict.keys()):  
                if (weaponname.lower() == weapon_dict[i]):
                    weaponid = i
                    break

        return weaponid

    def getserver(self, snippet):
        server = ""
        response = requests.get('https://tone.sleepycat.date/v2/client/servers').json()
        servers = response.keys()

        for i in servers:
            if(snippet in i.lower()):
                server = i

        return server

async def setup(client):
    await client.add_cog(Stats(client))

