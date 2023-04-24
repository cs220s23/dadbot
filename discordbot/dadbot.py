#!/usr/bin/env python3
import io
import sys
import os
from asyncio import sleep

import discord
import dotenv

from PIL import Image

from discord.ext import commands
from jokes import *
import memes


dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# jokes = FileJokes("jokes.txt")
jokes = RedisJokes(REDIS_HOST, int(REDIS_PORT))

@bot.event
async def on_ready():
        print(f'{bot.user} is online')
        print(f'Using {jokes.__class__} as joke source')
        print('#############')

@bot.command()
async def ping(ctx):
    """Responds to ping with pong"""
    await ctx.send("pong")
    print(f"{ctx.author} pinged")

@bot.command()
async def joke(ctx):
    """Tells jokes from a file"""
    for part in jokes.tell_joke():
        await ctx.send(part)
        await sleep(1)

@bot.command()
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

@bot.command()
async def winning(ctx, *message):
    """Pastes the users avatar on top of a meme"""
    message = ' '.join(message)
    meme_file = f"/tmp/{ctx.author.name}_winning.png"
    data = io.BytesIO(await ctx.author.avatar.read())
    img = Image.open(data)
    memes.winning(img, message, name=ctx.author.name).save(meme_file, format="png")
    await ctx.send(file=discord.File(meme_file))
    os.remove(meme_file)


if __name__ == "__main__":
    if DISCORD_TOKEN == None:
        sys.exit("Missing token")

    bot.run(DISCORD_TOKEN)
