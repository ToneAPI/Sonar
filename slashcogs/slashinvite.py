import discord
from discord.ext import commands
from discord import app_commands

class SlashInvite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashInvite.py is ready")

    @app_commands.command(name="invite", description="Tells you in how many servers sonar is active and gives an invite link with it")
    async def invite(self, interaction: discord.Interaction):
        link = "https://discord.com/api/oauth2/authorize?client_id=1100115547515011182&permissions=414464862272&scope=bot"
        await interaction.response.send_message("I'm already in " + str(len(self.client.guilds)) + " servers!\n" + "Invite me now using:\n " + link)

async def setup(client):
    await client.add_cog(SlashInvite(client))