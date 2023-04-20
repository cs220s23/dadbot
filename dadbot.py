#!/usr/bin/env python3
import sys
import os
from asyncio import sleep

import discord
import dotenv

from discord.ext import commands
from jokes import *


dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

jokes = Jokes("jokes.txt")

@bot.event
async def on_ready():
        print(f'{bot.user} is online')
        print('#############')

@bot.command()
async def ping(ctx):
    """Responds to ping with pong"""
    await ctx.send("pong")

@bot.command()
async def joke(ctx):
    """Tells jokes from a file"""
    for part in jokes.tell_joke():
        await ctx.send(part)
        await sleep(1)

if __name__ == "__main__":
    if DISCORD_TOKEN == None:
        sys.exit("Missing token")

    bot.run(DISCORD_TOKEN)
