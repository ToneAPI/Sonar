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
    async def leaderboard(self, ctx, message, weapon=""):
        message = message.lower()
        weaponid = ""
        botmessage = "Leaderboard of " + message + "\n"
        if(weapon != ""):
            weaponid = self.getweaponid(weapon)
            message = message[:-1]
            if(message != "deaths"):
                inbetween = " with "    
            else: 
                inbetween = " to "    
            botmessage = "Leaderboard of " + message + inbetween + weapon + "\n"
        
        if(str(message) not in ["kills", "deaths", "max_distance", "total_distance"]):
            await ctx.send('```This filter doesnt exist```')
        print(message)
        

        payload = {"weapon": weaponid}
        response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
        players = response.keys()

        top10 = []
        while(len(top10)<10):
            current = 0
            name = ""
            for p in players:
                stats = response[p]
                checked = stats[str(message)]
                if(checked > current and str(stats["username"] +": " + str(stats[str(message)])) not in top10):
                     current = checked
                     name = stats['username']
            top10.append(name+ ": " + str(current))

        counter = 1
        for i in top10:
            botmessage = botmessage + str(str(counter) + " - " + i + "\n")
            counter= counter+1 

        await ctx.send(f'```{botmessage}```')

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

async def setup(client):
    await client.add_cog(Leaderboard(client))