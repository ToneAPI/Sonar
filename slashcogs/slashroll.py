import discord
from discord import app_commands
from discord.ext import commands
import random

class SlashRoll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("SlashRoll.py is ready")

    @app_commands.command(name="roll", description="Rolls a number between 1 and 100 with a rating")
    async def slashroll(self, interaction: discord.Interaction):
        rolled = random.randint(1,100)
        rating = ""

        if(rolled == 100):
            rating = "What a chad"
        elif(rolled < 100 and rolled > 90):
            rating = "Almost"
        elif(rolled <= 90 and rolled > 80):
            rating = "Good"
        elif(rolled <= 80 and rolled > 69):
            rating = "Alright"
        elif(rolled == 69):
            rating = "Nice"
        elif(rolled < 69 and rolled > 50):
            rating = "Decent"
        elif(rolled <= 50 and rolled > 25):
            rating = "Meh"
        elif(rolled <= 25 and rolled > 1):
            rating = "Bad"
        elif(rolled == 1):
            rating = "LOL"

        message = "You rolled " + str(rolled) + ", " + rating

        await interaction.response.send_message(message)


async def setup(client):
    await client.add_cog(SlashRoll(client))