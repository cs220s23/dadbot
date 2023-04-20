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

async def timer(ctx, time):
    """Starts a timer for a set amount of time in seconds, then pings the calling user"""
    try:
        time = float(time)
    except ValueError:
        await ctx.send("Unrecognized time format")
        return

    await ctx.send(f'Starting timer for {time} seconds')
    print(f"Timer Started for {time} by {ctx.author}")
    await sleep(time)
    await ctx.send(f'Time\'s up {ctx.author.mention} !')
    print("Timer finished")

if __name__ == "__main__":
    if DISCORD_TOKEN == None:
        sys.exit("Missing token")

    bot.run(DISCORD_TOKEN)
