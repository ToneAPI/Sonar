import discord
from discord.ext import commands
from discord import app_commands

class SlashHelp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashHelp.py is ready")

    @app_commands.command(name="help", description= "Gives information about the commands in this bot")
    async def help(self, interaction: discord.Interaction, message:str ="all"):
        botmessage = ""
        if(message == "all"):
            botmessage = str("To get further information about a command do: \n!help <command> \n------------------- \n" +
                         "The commands you can get information on are: \n" + 
                         "changelog    : Gives all the information about the changes and updates.\n"
                         "roll         : Rolls a number between 1 and 100. \n" +
                         "ping         : Shows latency. \n" +
                         "stats        : Shows stats collected by ToneAPI. \n" +
                         "leaderboard  : Shows a leaderboard of stats. \n"+
                         "slashcommands: This explains what slash commands are, if you used slash commands before this isnt usefull\n"
                         "------------------- \n"
                         "if this help command doesnt help you or you have suggestions for future commands, ping or dm me @lars#1029")
        elif(message == "changelog"):
            botmessage = str("!changelogs is a command that gives you all the recent changes and updates")
        elif(message == "roll"):
            botmessage = str("!roll is a command that rolls a number between 1 and 100, with a rating")

        elif(message == "ping"):
            botmessage = str("!ping gives the latency between you and the bot")

        elif(message == "stats"):
            botmessage = str("!stats takes playername(s), Optional: weaponname, servername\n"+
                             "Example: \n!stats iilars, kraber, fvnkhead's 3v3 \n!stats <playername>, <weaponname>, <servername> \nA weapon or server doesnt need to be specified, because if they arent there it will take overall\n"+
                             "-------------------------------------------------\n"+
                             "For those wondering why the kd with a weapon doesnt match the webclient,\nthe webclient takes kills with a weapon and deaths to that weapon and this bot takes kills with weapon and deaths while weapon is held")
            
        elif(message == "leaderboard"):
            botmessage = str("!leaderboard is a leaderboard that can be filtered, also for the lazy between us leaderboard can be subsituted by lb, rank, ranking, board \n"
                             +"currently the leaderboard can only be filtered by kills, deaths, maxd, totald, kd and avgd with a specified weapon \n" +
                             "Example: \n!lb kills, kraber, fvnkhead's 3v3  \n!lb <filter>, <weaponname>, <servername> \nA weapon or server doesnt need to be specified\n"+
                             "------------------------\n"+
                             "maxd = max distance, avgd = average distance, kd = kill/death ratio and totald = total distance"
                             )
        elif(message == "slashcommands"):
             botmessage = str("To do a slash command, hit the / key and navigate to the sonar icon after doing this you will see all the commands.\nThese commands take the same input as the normal !commands")
        else:
            botmessage = "Cant help you with this"
            
        await interaction.response.send_message(f"```{botmessage}```")


async def setup(client):
    await client.add_cog(SlashHelp(client))