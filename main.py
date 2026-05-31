import discord
from discord.ext import commands
import json
import os

def get_prefix(bot, message):
    if not os.path.exists('prefixes.json'):
        return 'b!'
    with open('prefixes.json', 'r') as f:
        try:
            prefixes = json.load(f)
            return prefixes.get(str(message.guild.id), 'b!')
        except:
            return 'b!'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# This loads the help.py file
async def setup():
    await bot.load_extension('help')

import asyncio
async def run_bot():
    await setup()
    await bot.start('YOUR_BOT_TOKEN_HERE')

asyncio.run(run_bot())
