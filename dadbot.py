#!/usr/bin/env python3
import sys
import os
import discord
import dotenv

from discord.ext import commands


dotenv.load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
        print(f'{bot.user} is online')
        print('#############')

@bot.command()
async def ping(ctx):
    """Responds to ping with pong"""
    await ctx.send("pong")

if __name__ == "__main__":
    if DISCORD_TOKEN == None:
        sys.exit("Missing token")

    bot.run(DISCORD_TOKEN)
