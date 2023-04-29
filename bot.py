from discord.ext import commands
from discord import app_commands
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

async def slashload():
    for filename in os.listdir("./slashcogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"slashcogs.{filename[:-3]}")

@client.command()
async def sync(ctx):
    if ctx.message.author.id == 262672220260663297:
        await client.tree.sync(guild=discord.Object(id=1100149380763373608))
        print('Command tree synced.')
    else:
        await ctx.send('You must be the botowner to use this command!')
                                        
async def main():
    async with client:
        await load()
        await slashload()
        await client.start(discordtoken.get())

asyncio.run(main())