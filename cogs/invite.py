

import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Invite.py is ready")

    @commands.command()
    async def invite(self, ctx):
        link = "https://discord.com/api/oauth2/authorize?client_id=1100115547515011182&permissions=414464862272&scope=bot"
        await ctx.send("I'm already in " + str(len(self.client.guilds)) + " servers!\n" + "Invite me now using:\n " + link)

async def setup(client):
    await client.add_cog(Invite(client))