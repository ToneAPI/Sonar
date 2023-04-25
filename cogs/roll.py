import discord
from discord.ext import commands
import random

class Roll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("roll.py is ready")

    @commands.command()
    async def roll(self, ctx):
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

        await ctx.send(message)


async def setup(client):
    await client.add_cog(Roll(client))