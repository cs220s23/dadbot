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
JOKE_FILE = os.getenv('JOKE_FILE')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.jokes = None

@bot.event
async def on_ready():
    logger.info(f'{bot.user} is online')
    logger.info(f'Attempting to establish redis connection')
    try:
        bot.jokes = RedisJokes(REDIS_HOST, int(REDIS_PORT))
        bot.jokes.r.ping()
        logger.info(f'Connection to {REDIS_HOST}:{REDIS_PORT} successful')
        if JOKE_FILE is None:
            logger.warning(f'Default joke source not set, defaulting to "jokes.txt"')
            joke_file = 'jokes.txt'
        else:
            joke_file = JOKE_FILE
        bot.jokes.read_from_file(joke_file)
    except ConnectionError:
        logger.warning('Cannot connect to redis, defaulting to "bot.jokes.txt"')
        bot.jokes = FileJokes("jokes.txt")
    logger.info(f'Using {bot.jokes.source()} as joke source')

@bot.command()
async def ping(ctx):
    """Responds to ping with pong"""
    await ctx.send("pong")
    logger.info(f"{ctx.author} pinged")

@bot.command()
async def joke(ctx):
    """Tells jokes"""
    for part in bot.jokes.tell_joke():
        await ctx.send(part)
        await sleep(1)

@bot.command()
async def jokeadd(ctx, *joke):
    """Adds a joke to the joke store"""
    if bot.jokes.source() == "RedisJokes":
        joke_parts = tuple( j.strip() for j in ' '.join(joke).split('|'))
        bot.jokes.add_joke(joke_parts)
        logger.info(f'{ctx.author} added joke {bot.jokes.r.scard("jokes")} to the joke database')
    else:
        await ctx.send(f"Reading Jokes from {bot.jokes.source()}, cannot add jokes to that source")

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
