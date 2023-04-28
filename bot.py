from discord.ext import commands
import discord
import os
import asyncio
from discordtoken import discordtoken

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    print("Succes: Bot has started working")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(discordtoken.get())

asyncio.run(main())