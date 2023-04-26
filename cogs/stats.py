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
    async def stats(self, ctx, message="any player", message2="any weapon"):  
        if(message != "any player"):
            if(message2 != "any weapon"):
                message = message[:-1]
                print(message + "\n"  + message2)
                weaponid = self.getweaponid(message2)
            
            playerid = self.getplayerid(message);

            if (playerid != ""):
                print("test: " + weaponid)
                payload = {'player': playerid, 'weapon': weaponid}
                response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
                killstats = response[playerid]
                print(response)
                botmessage = str("Playername: " + killstats['username'] + '\n' + "Kills: " + str(killstats['kills']) + '\n' )
                
                if(weaponid != ""):
                    botmessage += str("Deaths: " + str(killstats['deaths_while_equipped'])) + '\n' + str("Weapon: " + message2) + '\n' + str(str("KD with weapon: " + str("{:0.2f}".format(killstats['kills']/killstats['deaths_while_equipped']))))
                else:
                    botmessage = botmessage + str("Deaths: " + str(killstats['deaths'])) + '\n' + str("KD: " + str("{:0.2f}".format(killstats['kills']/killstats['deaths'])))
                print(botmessage)
            else:
                botmessage = "This player doesnt exist"
        else:
            botmessage = "No name given"

        await ctx.send(botmessage)

    def getplayerid(self, playername):
        response = requests.get('https://tone.sleepycat.date/v2/client/players').json()
        r = response.keys()
        playerid = ""
        for i in r:
            p = response[i]['username']
            if (p.lower() == playername.lower()):
                playerid = i
                break

        print(playername + ": " + str(playerid))
        return playerid

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
        print(weaponname + ', '+ weaponid)
        return weaponid

async def setup(client):
    await client.add_cog(Stats(client))

