import datetime
import discord
from discord.ext import tasks, commands
import asyncio
import json
from discord.ext.commands.context import Context
import requests
import websockets
import colorama
from colorama import Fore

class Websocket(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.websocket.start()

    def cog_unload(self):
        print("websocket got unloaded")
        self.websocket.cancel()

    @tasks.loop(seconds=5)
    async def websocket(self, ws):
        async for message in ws:
            if (message == "ping"):
                print("pong\n")
                await ws.send("pong")
            else:
                await self.message_handler(message)

    @websocket.before_loop
    async def before_websocket(self):
        print('waiting... for bot to start. (websocket)')
        uri = "wss://tone.sleepycat.date/v2/client/websocket"
        global atkerlist
        global victimlist
        atkerlist = []
        victimlist = []
        async with websockets.connect(uri) as ws:
            await self.websocket(ws)
        await self.bot.wait_until_ready()

    async def message_handler(self, message):
        try:
            message = json.loads(message)
            weapons = {'human_execution': 'execution', 'mp_weapon_car': 'car', 'mp_weapon_defender': 'charge rifle', 'mp_weapon_doubletake': 'double take', 'mp_weapon_epg': 'epg', 'mp_weapon_hemlok_smg': 'volt', 'mp_weapon_lstar': 'lstar', 'mp_weapon_r97': 'r97', 'mp_weapon_rspn101': 'r-201', 'mp_weapon_smart_pistol': 'smart pistol', 'mp_weapon_sniper': 'kraber', 'mp_weapon_vinson': 'flatline', 'mp_weapon_autopistol': 're-45 auto', 'mp_weapon_alternator_smg': 'alternator', 'mp_weapon_frag_grenade': 'frag grenade', 'mp_weapon_g2': 'g2', 'mp_weapon_lmg': 'spitfire', 'mp_weapon_smr': 'smr', 'mp_weapon_softball': 'softball', 'mp_weapon_thermite_grenade': 'firestar', 'melee_pilot_emptyhanded': 'melee', 'mp_weapon_mastiff': 'masstiff', 'mp_weapon_mgl': 'mgl', 'mp_weapon_rspn101_og': 'r-101', 'mp_weapon_wingman': 'wingman', 'invalid': 'invalid', 'mp_weapon_arc_launcher': 'thunderbolt', 'mp_weapon_dmr': 'dmr', 'mp_weapon_grenade_electric_smoke': 'electric smoke', 'mp_weapon_pulse_lmg': 'cold war', 'mp_weapon_satchel': 'satchel', 'mp_weapon_shotgun': 'eva-8 auto', 'mp_weapon_shotgun_pistol': 'mozambique', 'mp_weapon_wingman_n': 'wingman elite', 'mp_weapon_grenade_gravity': 'gravity star', 'mp_weapon_grenade_sonar': 'pulse blade', 'mp_weapon_rocket_launcher': 'archer', 'outOfBounds': 'outOfBounds', 'mind_crime': 'mind crime', 'mp_weapon_esaw': 'devotion', 'fall': 'fall', 'mp_weapon_semipistol': 'p2016', 'mp_weapon_grenade_emp': 'arc grenade', 'mp_weapon_hemlok': 'hemlok', 'phase_shift': 'phase shift'}
            weapon = ""
            try: 
                weapon = weapons[message["cause_of_death"]] 
            except KeyError: 
                weapon = message["cause_of_death"]

            botmessage = discord.Embed(title="Sonar", description="", colour=discord.Colour.orange())
            if(requests.head(f"https://toneapi.github.io/ToneAPI_webclient/weapons/{message['cause_of_death']}.png").status_code == 200):
                botmessage.set_image(url=f"https://toneapi.github.io/ToneAPI_webclient/weapons/{message['cause_of_death']}.png")
            else:
                botmessage.set_image(url="https://toneapi.github.io/ToneAPI_webclient/weapons/notfound.png")

            atkerlist.append(message['attacker_name'])
            victimlist.append(message['victim_name'])

            if(message['attacker_name'] in victimlist):
                delete = message['attacker_name']
                while(delete in victimlist):
                    index = victimlist.index(delete)
                    victimlist.pop(index)

            if(message['victim_name'] in atkerlist):
                delete = message['victim_name']
                while(delete in atkerlist):
                    index = atkerlist.index(delete)
                    atkerlist.pop(index)

            date_time = datetime.datetime.now()
            time = str(date_time)[11:16]
            date = str(date_time)[0:10]
            botmessage.add_field(name="Attacker", value=f"{message['attacker_name']}", inline=True)
            botmessage.add_field(name="Victim", value=f"{message['victim_name']}" ,inline=True)
            botmessage.add_field(name="weapon", value=f"{weapon}" ,inline=False)
            botmessage.add_field(name="killstreak", value=f"{atkerlist.count(message['attacker_name'])}" ,inline=True)
            botmessage.add_field(name="deathstreak victim", value=f"{victimlist.count(message['victim_name'])}" ,inline=True)
            botmessage.add_field(name="Server", value=f"{message['servername']}",inline=False)
            botmessage.set_footer(text=f"Brought to you by ToneAPI.\nCreated at {time} GMT+2 " + f"on the date {date}")
            
            if("[V3X]" in message['servername']):
                channel = self.bot.get_channel(1107308328146714705)
                await channel.send(embed=botmessage)
            if("fvnk" in message['servername']):
                channel = self.bot.get_channel(1107308250182991892)
                await channel.send(embed=botmessage)
            if("ikhadhonger" in message['servername']):
                channel = self.bot.get_channel(1107308352586911875)
                await channel.send(embed=botmessage)
            if(atkerlist.count(message['attacker_name']) > 5):
                channel = self.bot.get_channel(1107681478587973693)
                await channel.send(embed=botmessage)

            print(str(f"{message['attacker_name']}" + "killed" +f"{message['victim_name']}" + " with " + f"{weapon}" + " on " + f"{message['servername']}" + "\n" + f"Killstreak {atkerlist.count(message['attacker_name'])}" + " " + f"Deathstreak {victimlist.count(message['victim_name'])}") + " " + f"Created at {time} GMT+2 " + f"on the date {date}"+"\n")
            channel = self.bot.get_channel(1107308531553685534)
            await channel.send(embed=botmessage)
        except Exception as e:
            print(Fore.RED + e)

    @commands.command()
    async def start_killfeed(self, ctx):
        if ctx.message.author.id == 262672220260663297:
            self.websocket.start()
            await ctx.send("Killfeed got started")
        else:
            await ctx.send('You must be the botowner to restart killfeed!')
    
    @commands.command()
    async def cancel_killfeed(self, ctx):
        if ctx.message.author.id == 262672220260663297:
            self.websocket.cancel()
            await ctx.send("killfeed got stopped")
        else:
            await ctx.send('You must be the botowner to stop killfeed!')
    
    @commands.command()
    async def change_interval_killfeed(self, ctx, seconds):
        if ctx.message.author.id == 262672220260663297:
            self.websocket.change_interval(seconds=seconds)
            await ctx.send(f"Killfeed now sends every {seconds} seconds")
        else:
            await ctx.send('You must be the botowner to change the interval of the killfeed!')



async def setup(client):
    await client.add_cog(Websocket(client))
