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

    
    def getleaderboard(self, board:str, weaponid="", weaponname="", server=""):
        payload = {"weapon": weaponid, "server": server}
        response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
        players = response.keys()
        if(board.lower() == "totald"):
            board = "total_distance"
        elif(board.lower() == "maxd"):
            board = "max_distance"
        
        if(board.lower() == "kd"):
            handler = lambda p : response[p]['kills'] / max(response[p].deaths, 1)
        elif(board.lower() == "avgd"):
            handler = lambda p : response[p]['total_distance'] / max(response[p].kills, 1)
        else:
            if(board.lower() not in ['username', 'deaths','kills', 'max_distance','total_distance']):
                raise Exception("Key " + board.lower() + ' not found for player leaderboard')
            handler = lambda p : response[p][board.lower()]
            
        result = sorted(players, key=handler, reverse=True)[:10]

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
        for p in result:
            botmessage = botmessage + str(f"{str(counter):<2}"+ " - " + f"{response[p]['username'] :<20}" + " : "+ f"{str(handler(p)):<8}" + "\n")
            counter= counter+1 
        return botmessage

async def setup(client):
    await client.add_cog(Leaderboard(client))