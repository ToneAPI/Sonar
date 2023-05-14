import asyncio
from urllib import request
import aiohttp
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
        server = ""
        weaponid = ""
        weaponname = ""

        if(message == ()):
            error = True
            await ctx.send("```No player given```")
            return
        
        message = list(message)
        message = "".join(message)
        message = message.split(",")

        async with aiohttp.ClientSession() as session:
            players, residue = await self.get_all_playerids(session, message)

            for item in residue:
                if(server == "" and item != None and item != ""):
                    server = await self.getserver(item)
                if(weaponid == "" and item != None and item != ""):
                    weaponid, weaponname = self.getweaponid(item)
            

        if(len(players.values()) == 0 and error == False):
            error = True
            await ctx.send("```No existing player found, check if the name is correct or has changed\n\n*Note you need to split filters with a comma```")
            return

        async with aiohttp.ClientSession() as session:
            stats = await self.get_allplayer_stats(session, players.values(), weaponid, weaponname, server)

            if(server != ""):
                botmessage = str("Stats for " + server + "\n" + "-----------------------" + "\n") 
            else:
                botmessage = str("Stats for all servers\n" + "-----------------------" + "\n")

            botmessage = botmessage + str("\n-----------------------\n".join(stats))

        await ctx.send(f"```{botmessage}```")


    async def get_all_playerids(self, s, playernames):
     players = {}
     residue = []
     tasks = []
     for playername in playernames:
          task = asyncio.create_task(self.getplayerid(s, playername),name=playername)
          tasks.append(task)
     res = await asyncio.gather(*tasks)
     for player in res:
           player = player.split(":")
           playername = player[0].strip()
           playerid = player[1].strip()
           if(playerid != "None" and playername not in players):
                players[playername] = playerid
           else:
                residue.append(playername) 
     return players, residue

    async def getplayerid(self,s,playername):
        playerid = ""
        playername = playername.replace(",", "")
        payload = str(f"?username={playername}")
        async with s.get(f'https://northstar.tf/accounts/lookup_uid{payload}') as r:
                
                response = await r.json()
                if (response['matches'] != None and response['matches'] != []):
                    playerid = response['matches'][0]
                    player = str(f"{playername.lower()}: {playerid}")
                else:
                    player = str(f"{playername.lower()}: {None}")
                return player
        
    def getweaponid(self,weaponname):
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
                    "mastiff": "mp_weapon_mastiff",
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

    async def getserver(self, snippet):
        server = ""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://tone.sleepycat.date/v2/client/servers') as r:
                response = await r.json()
                servers = response.keys()

        for i in servers:
            if(snippet.lower() == i.lower().replace(" ", "")):
                server = i
                break
            elif(snippet.lower() in i.lower().replace(" ", "")):
                 server = i

        return server

    async def get_allplayer_stats(self, s, playerids, weaponid = "", weaponname= "",server = ""):
     tasks = []
     for playerid in playerids:
          task = asyncio.create_task(self.getstats(s, playerid, weaponid, weaponname, server), name=playerid)
          tasks.append(task)
     res = await asyncio.gather(*tasks)
     return res

    async def getstats(self, s, playerid, weaponid = "", weaponname = "", server = ""):
        payload = {'player': playerid, 'weapon': weaponid, 'server': server}
        async with s.get('https://tone.sleepycat.date/v2/client/players', params=payload) as r:
            response = await r.json()
            if(response == {}):
                async with s.get("https://northstar.tf/accounts/get_username", params={"uid": playerid}) as Er:
                    errorresponse = await Er.json()
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

