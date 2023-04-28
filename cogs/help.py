import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help.py is ready")

    @commands.command()
    async def help(self, ctx, message="all"):
        botmessage = ""
        if(message == "all"):
            botmessage = str("To get further information about a command do: \n!help <command> \n" +
                         "The commands you can get information on are: \n" + 
                         "roll \n" +
                         "ping \n" +
                         "compare \n" +
                         "stats \n" +
                         "leaderboard \n"+
                         "------------------- \n"
                         "if this help command doesnt help you or you have suggestions for future commands, ping or dm me @lars#1029")
        elif(message == "roll"):
            botmessage = str("!roll is a command that rolls a number between 1 and 100, with a rating")
        elif(message == "ping"):
            botmessage = str("!ping gives the latency between you and the bot")
        elif(message == "compare"):
            botmessage = str("!compare takes multiple playernames and 1 weapon to compare these players \n"+
                             "Example: \n!compare iilars, legonzaur, okvdai, kraber \n!compare <playername>, <playername>, <playername>, <weaponname> \nA weapon doesnt need to be specified")
        elif(message == "stats"):
            botmessage = str("!stats takes 1 playername and 1 weapon name to show this players stats\n"+
                             "Example: \n!stats iilars, kraber \n!stats <playername>, <weaponname> \nA weapon doesnt need to be specified\n"+
                             "For those wondering why the kd with a weapon doesnt match the webclient, de webclient takes kills with a weapon and deaths to that weapon and this bot takes kills with weapon and deaths while weapon is held")
        elif(message == "leaderboard"):
            botmessage = str("!leaderboard is a leaderboard that can be filtered, also for the lazy between us leaderboard can be subsituted by lb, rank, ranking \n"
                             +"currently the leaderboard can only be filtered by kills, deaths, max_distance, total_distance with a specified weapon \n" +
                             "Example: \n!lb kills, kraber  \n!lb <filter>, <weaponname> \nA weapon doesnt need to be specified")
        else:
            botmessage = "Cant help you with this"
            
        await ctx.send(f"```{botmessage}```")


async def setup(client):
    await client.add_cog(Help(client))