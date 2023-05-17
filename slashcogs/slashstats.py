import asyncio
import aiohttp
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
        server = ""
        weaponid = ""
        weaponname = ""

        playernames = playernames.replace(",", " ")
        playernames = playernames.split(" ")

        async with aiohttp.ClientSession() as session:
            players = await self.get_all_playerids(session, playernames)
            if(players == {} or players.keys() == []):
                await interaction.response.send_message("```No existing player given.\nIf you put in multiple players make sure to split them with a comma(,)```")
                return

            if(weapon != ""):
                weaponid, weaponname = self.getweaponid(weapon)
            if(servername != ""):
                server = await self.getserver(servername)

        async with aiohttp.ClientSession() as session:
            botmessage = await self.get_allplayer_stats(session, players.values(), weaponid, weaponname, server)

        await interaction.response.send_message(embed=botmessage)


    async def get_all_playerids(self, s, playernames):
     players = {}
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

     return players

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
        
    def getweaponid(self,givenweapon):
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
        weaponname = ""
        for weapon in weapons:     
            if(givenweapon.lower() in weapon.lower()):     
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
            if(snippet.lower() == i.lower()):
                server = i
                break
            elif(snippet.lower() in i.lower()):
                 server = i

        return server

    async def get_allplayer_stats(self, s, playerids, weaponid = "", weaponname= "",server = ""):
        tasks = []
        for playerid in playerids:
            task = asyncio.create_task(self.getstats(s, playerid, weaponid, server), name=playerid)
            tasks.append(task)
        res = await asyncio.gather(*tasks)
        if(server == ""):
            server = "All"
        if(weaponname == ""):
            weaponname = "Any"

        botmessage = discord.Embed(title="Stats", description=f"**Server:** {server}\n**Weapon:** {weaponname}", colour=discord.Colour.orange())
        if(weaponname != "Any"):
            if(requests.head(f"https://toneapi.github.io/ToneAPI_webclient/weapons/{weaponid}.png").status_code == 200):
                botmessage.set_thumbnail(url=f"https://toneapi.github.io/ToneAPI_webclient/weapons/{weaponid}.png")
            else:
                botmessage.set_thumbnail(url="https://toneapi.github.io/ToneAPI_webclient/weapons/notfound.png")

        for stats in res:
            botmessage.add_field(name=f"Stats for {stats['Player']}", value=stats['message'])
            
        return botmessage

    async def getstats(self, s, playerid, weaponid = "", server = ""):
        payload = {'player': playerid, 'weapon': weaponid, 'server': server}
        async with s.get('https://tone.sleepycat.date/v2/client/players', params=payload) as r:
            response = await r.json()
            if(response == {}):
                async with s.get("https://northstar.tf/accounts/get_username", params={"uid": playerid}) as Er:
                    errorresponse = await Er.json()
                    if(errorresponse['matches'] != None):
                        playername = errorresponse['matches'][0]
                        stats = {"Player": playername, "message": "No stats found for this player."}
                        return stats
        
            killstats = response[str(playerid)]

            botmessage = str("Kills: " + str(killstats['kills']) + '\n' )
              
            if(weaponid != ""):
                deaths=killstats['deaths_while_equipped']
                if(deaths == 0):
                    deaths = 1;
                botmessage += str(str("Deaths: " + str(killstats['deaths_while_equipped'])) + '\n' + str(str("weapon KD : " + str("{:0.2f}".format(killstats['kills']/deaths)))+ '\n' + str("Deaths to: " + str(killstats['deaths']))))
            else:
                deaths=killstats['deaths']
                if(deaths == 0):
                    deaths = 1;
                botmessage = botmessage + str("Deaths: " + str(killstats['deaths'])) + '\n' + str("KD: " + str("{:0.2f}".format(killstats['kills']/deaths)))

        stats = {"Player": killstats['username'], "message": botmessage}
        
        return stats
    
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
        async with aiohttp.ClientSession() as session:
            async with session.get('https://tone.sleepycat.date/v2/client/servers') as r:
                servers = await r.json()

        for server_choice in servers.keys():
            if(current.lower() in server_choice.lower()):
                data.append(app_commands.Choice(name=server_choice, value=server_choice))
        return data
    

async def setup(client):
    await client.add_cog(SlashStats(client))

