import discord
from discord.ext import tasks, commands
import asyncio
import json
from discord.ext.commands.context import Context
import websockets


class Websocket(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.websocket.start()

    def cog_unload(self):
        self.websocket.cancel()

    @tasks.loop(seconds=5)
    async def websocket(self):
        uri = "wss://tone.sleepycat.date/v2/client/websocket"
        async with websockets.connect(uri) as ws:
            async for message in ws:
                if (message == "ping"):
                    await ws.send("pong")
                else:
                    await self.message_handler(message)

    @websocket.before_loop
    async def before_websocket(self):
        print('waiting... for bot to start. (websocket)')
        await self.bot.wait_until_ready()

    async def message_handler(self, message):
        message = json.loads(message)
        weapons = {'human_execution': 'execution', 'mp_weapon_car': 'car', 'mp_weapon_defender': 'charge rifle', 'mp_weapon_doubletake': 'double take', 'mp_weapon_epg': 'epg', 'mp_weapon_hemlok_smg': 'volt', 'mp_weapon_lstar': 'lstar', 'mp_weapon_r97': 'r97', 'mp_weapon_rspn101': 'r-201', 'mp_weapon_smart_pistol': 'smart pistol', 'mp_weapon_sniper': 'kraber', 'mp_weapon_vinson': 'flatline', 'mp_weapon_autopistol': 're-45 auto', 'mp_weapon_alternator_smg': 'alternator', 'mp_weapon_frag_grenade': 'frag grenade', 'mp_weapon_g2': 'g2', 'mp_weapon_lmg': 'spitfire', 'mp_weapon_smr': 'smr', 'mp_weapon_softball': 'softball', 'mp_weapon_thermite_grenade': 'firestar', 'melee_pilot_emptyhanded': 'melee', 'mp_weapon_mastiff': 'masstiff', 'mp_weapon_mgl': 'mgl', 'mp_weapon_rspn101_og': 'r-101', 'mp_weapon_wingman': 'wingman', 'invalid': 'invalid', 'mp_weapon_arc_launcher': 'thunderbolt', 'mp_weapon_dmr': 'dmr', 'mp_weapon_grenade_electric_smoke': 'electric smoke', 'mp_weapon_pulse_lmg': 'cold war', 'mp_weapon_satchel': 'satchel', 'mp_weapon_shotgun': 'eva-8 auto', 'mp_weapon_shotgun_pistol': 'mozambique', 'mp_weapon_wingman_n': 'wingman elite', 'mp_weapon_grenade_gravity': 'gravity star', 'mp_weapon_grenade_sonar': 'pulse blade', 'mp_weapon_rocket_launcher': 'archer', 'outOfBounds': 'outOfBounds', 'mind_crime': 'mind crime', 'mp_weapon_esaw': 'devotion', 'fall': 'fall', 'mp_weapon_semipistol': 'p2016', 'mp_weapon_grenade_emp': 'arc grenade', 'mp_weapon_hemlok': 'hemlok', 'phase_shift': 'phase shift'}
        weapon = ""
        try: 
            weapon = weapons[message["attacker_current_weapon"]] 
        except KeyError: 
            weapon = message["attacker_current_weapon"]

        botmessage = discord.Embed(title="Sonar", description="", colour=discord.Colour.orange())
        # try:
        #     img_weapon = discord.File(f"./images/{message['attacker_current_weapon']}.png", filename=f"{message['attacker_current_weapon']}.png")
        #     botmessage.set_image(url=f"attachment://{message['attacker_current_weapon']}.png")
        # except FileNotFoundError:
        #     img_weapon = discord.File("./images/notfound.png", filename="notfound.png") 
        #     botmessage.set_image(url="attachment://notfound.png")
        # img_weapon = discord.File("./images/mp_weapon_sniper.png", filename="mp_weapon_sniper.png")
        # botmessage.set_image(url="attachment://mp_weapon_sniper.png")
        botmessage.add_field(name="Attacker", value=f"{message['attacker_name']}", inline=True)
        botmessage.add_field(name="Victim", value=f"{message['victim_name']}" ,inline=True)
        botmessage.add_field(name="weapon", value=f"{weapon}" ,inline=False)
        botmessage.add_field(name="Server", value=f"{message['servername']}",inline=False)
        # botmessage.add_field(name="Image", value=f"attachment://{message['attacker_current_weapon']}.png" + "\n" + f"{message['attacker_current_weapon']}.png",inline=False)
        botmessage.set_footer(text="Brought to you by ToneAPI")
        
        # if("[V3X]" in message['servername']):
        #     channel = self.bot.get_channel(1107308328146714705)
        #     await channel.send(file=img_weapon, embed=botmessage)
        # if("fvnk" in message['servername']):
        #     channel = self.bot.get_channel(1107308250182991892)
        #     await channel.send(file=img_weapon, embed=botmessage)
        # if("ikhadhonger" in message['servername']):
        #     channel = self.bot.get_channel(1107308352586911875)
        #     await channel.send(file=img_weapon, embed=botmessage)

        channel = self.bot.get_channel(1107308531553685534)
        #file=img_weapon,
        await channel.send(embed=botmessage)



async def setup(client):
    await client.add_cog(Websocket(client))
