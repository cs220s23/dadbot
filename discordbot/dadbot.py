#!/usr/bin/env python3
import io
import sys
import os
from asyncio import sleep

import discord
import dotenv

from PIL import Image

from discord.ext import commands
from redis import ConnectionError
from jokes import *
import logging
import memes

logger = logging.getLogger('discord')

dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

try:
    logger.info("Connecting to redis")
    jokes = RedisJokes(REDIS_HOST, int(REDIS_PORT))
    jokes.r.ping()
except ConnectionError:
    logger.warning('Cannot connect to redis, defaulting to "jokes.txt"')
    jokes = FileJokes("jokes.txt")

@bot.event
async def on_ready():
    logger.info(f'{bot.user} is online')
    logger.info(f'Using {jokes.source()} as joke source')

@bot.command()
async def ping(ctx):
    """Responds to ping with pong"""
    await ctx.send("pong")
    logger.info(f"{ctx.author} pinged")

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
        logger.error(f"Unrecognized time format {time}")
    else:
        await ctx.send(f'Starting timer for {time} seconds')
        logger.info(f"Timer Started for {time} by {ctx.author}")
        await sleep(time)
        await ctx.send(f'Time\'s up {ctx.author.mention} !')
        logger.info(f"Timer started by {ctx.author} ended after {time} seconds")

@bot.command()
async def winning(ctx, *message):
    """Pastes the users avatar on top of a meme"""
    message = ' '.join(message)
    meme_file = f"/tmp/{ctx.author.name}_winning.png"
    data = io.BytesIO(await ctx.author.avatar.read())
    img = Image.open(data)
    memes.winning(img, message, name=ctx.author.name).save(meme_file, format="png")
    logger.info(f'Saving {meme_file} for {ctx.author}')
    await ctx.send(file=discord.File(meme_file))
    os.remove(meme_file)
    logger.info(f'Removing {meme_file}')


if __name__ == "__main__":
    if DISCORD_TOKEN is None or DISCORD_TOKEN == '':
        sys.exit("Missing token")

    bot.run(DISCORD_TOKEN)
