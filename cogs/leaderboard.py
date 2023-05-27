import discord
from discord.ext import commands
import requests
from Reuse.getServer import getserver

from Reuse.getWeapon import getweaponid

class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leaderboard.py is ready")

    @commands.command(aliases = ["lb", "board", "ranking", "rank"])
    async def leaderboard(self, ctx, *message):
        boards = ["kd", "avgd", "maxd", "totald","deaths", "kills"]
        error = False
        board = ""
        servers = []
        server = ""
        weaponid= ""
        weaponname= ""

        if(message == ()):
            error = True
            botmessage = "No leaderboard option selected, choose from:\n"
            for i in boards:
                botmessage = botmessage + i + "\n"
            await ctx.send(f"```{botmessage}```")

        message = list(message)
        message = "".join(message)
        message = message.split(",")

        print(message)

        for i in message:
            item = i.strip()
            if(item.lower() not in boards):
                function_dict = await self.message_handler(item)
                if(function_dict['weapon'] != None):
                    weaponname = function_dict["weapon"][1]
                    weaponid= function_dict['weapon'][0]
                if(function_dict['server'] != None):
                    servers.append(function_dict['server'])
            else:
                board = item 

        if(board == "" and error == False):
            error = True
            botmessage = "No leaderboard option selected, choose from:\n"
            for i in boards:
                botmessage = botmessage + i + "\n"

            botmessage = botmessage + "\n*Note you need to split filters with comma's(,)"
            await ctx.send(f"```{botmessage}```")

        servers.append(await getserver("", " ".join(message)))
        server = ""
        if(len(servers) > 1):   
            for i in servers:
                if(i.lower() in " ".join(message).lower()):
                    server = i
                    break   
                else:
                    server = servers[0]

        botmessage = self.getleaderboard(weaponid=weaponid, weaponname=weaponname, server=server, board=board)

        await ctx.send(f'```{botmessage}```')

    async def message_handler(self, message):
        weapon = False
        server = False
        return_message = {"weapon": None, "server": None}

        weaponid, weaponname = getweaponid(message)
        if(weaponid != ""):
            weapon = True

        servername = await getserver(message)
        if(servername != ""):
            server = True

        if(server):
            return_message["server"] = servername
        if(weapon):
            return_message["weapon"] = [weaponid, weaponname]

        return return_message

    
    def getleaderboard(self, board, weaponid="", weaponname="", server=""):
        easyfilter = False
        hardfilter = False
        payload = {"weapon": weaponid, "server": server}
        response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
        players = response.keys()

        if(board.lower() in ["kills", "deaths", "maxd", "totald"]):
            if(board.lower() == "totald"):
                board = "total_distance"
            if(board.lower() == "maxd"):
                board = "max_distance"       
            easyfilter = True
        else:
            hardfilter = True
        top10 = {}

        if(len(players) < 10):
            lb_length = len(players)
        else:
            lb_length = 10

        while(len(top10)<lb_length):
            current = 0 
            name = ""
            for p in players:
                stats = response[p]
                if(easyfilter):
                    checked = stats[str(board)]
                if(hardfilter):
                    if(board.lower() == "kd"):
                        if(weaponid != ""):
                            deaths = stats['deaths_while_equipped']
                        else:
                            deaths = stats['deaths']
                        if(deaths == 0):
                            deaths = deaths + 1
                        checked = round(stats["kills"] / deaths, 2)
                    if(board.lower() == "avgd"):
                        if(stats["kills"] == 0):
                            kills = 1
                        else:
                            kills = stats["kills"]
                        checked = round(stats["total_distance"] / kills, 2)
                #print(checked, ", ", current )
                if(checked >= current and stats["username"] not in top10.keys()):
                     #print(checked, ", ", current)
                     current = checked
                     name = stats['username']
        
            top10[name] = current

        if(board.lower() == "deaths"):
            inbetween = "to"
        else:
            inbetween = "with"

        if(server == ""):
            server = "all servers"
        if(weaponname == ""):
            weaponname = "any weapon"

        botmessage = str(f"Leaderboard of {board} {inbetween} {weaponname} for {server}\n-------------------------------\n")

        counter = 1
        for i, j in top10.items():
            if(hardfilter):
                stat = str("{:0.2f}".format(j))
            if(easyfilter):
                stat = str(j)
            botmessage = botmessage + str(f"{str(counter):<2}"+ " - " + f"{i :<20}" + " : "+ f"{stat:<8}" + "\n")
            counter= counter+1 

        return botmessage

async def setup(client):
    await client.add_cog(Leaderboard(client))