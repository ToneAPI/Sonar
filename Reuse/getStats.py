import asyncio

import discord
import requests

from Reuse.makePiechart import make_donut_chart
from Reuse.valuesChartGamemode import valueschartgamemode
from Reuse.valuesChartWeapon import valueschartweapon

async def get_allplayer_stats(s, playerids, weaponid = "", weaponname= "",server = ""):
        tasks = []
        for playerid in playerids:
            task = asyncio.create_task(getstats(s, playerid, weaponid, server), name=playerid)
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

        img_file = ""
        if(len(res) == 1):
            if(server == "All" and weaponname != "Any"):
                labels, values, colors = valueschartgamemode(playerid, weaponid)
            else: 
                labels, values, colors = valueschartweapon(playerid, server)
            botmessage, img_file = make_donut_chart(botmessage, labels, values, colors)
            return botmessage, img_file
        else:
            img_file = ""
            return botmessage, img_file
        
async def getstats(s, playerid, weaponid = "", server = ""):
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