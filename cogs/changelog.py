import discord
from discord.ext import commands

class Changelog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Changlog.py is ready")

    @commands.command()
    async def changelog(self, ctx):
     botmessage = str(
          "Welcome to V1.1 of Sonar, we have lots to discuss because alot has changed or got added.\n\n"+

          "-change 1, !stats and !compare arent 2 different functions anymore but became 1 function,\n"+
          "so now you can do !stats <playername>, <playername>, <weapon>, or for those who like to write !compare this still works aswell.\n\n"+

          "-change 2, !stats, !lb (!leaderboard) got <server> filters so now its possible to see your standing in a server.\n\n"

          "-change 3, All currently existing commands did get an overhaul to make them less restrictive to people, so you no longer need to write wingman_elite,\n"+
          "you can now do wingman elite or elite to get the wingman elite as filter, servers do have the same principle\n\n"+

          "-change 4, clearer error message\n\n"+

          "-change 5, All currently existing commands did get a slash command counterpart\n\n"+

          "Thanks for reading and goodluck increasing those stats"
     )
     await ctx.send(f"```{botmessage}```")


async def setup(client):
    await client.add_cog(Changelog(client))