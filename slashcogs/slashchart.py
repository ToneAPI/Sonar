import discord
from discord.ext import commands
from discord import app_commands

class SlashChart(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashPing.py is ready")

    @app_commands.command(name="chart", description="Gives a chart")
    async def slashchart(self, interaction: discord.Interaction, host : str, server : str = ""):
        img_file = ""
        botmessage = discord.Embed(title="Chart", description=f"**Host:** {host}", colour=discord.Colour.orange())


        
        if(img_file != ""):
            await interaction.response.send_message(embed=botmessage, file=img_file)
        else:
            await interaction.response.send_message(embed=botmessage)


async def setup(client):
    await client.add_cog(SlashChart(client))