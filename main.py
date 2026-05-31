import discord
from discord.ext import commands
import json
import os
import asyncio

def get_prefix(bot, message):
    if not os.path.exists('prefixes.json'): return 'b!'
    with open('prefixes.json', 'r') as f:
        try:
            prefixes = json.load(f)
            return prefixes.get(str(message.guild.id), 'b!')
        except: return 'b!'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# CRITICAL: This removes the default help so your custom one works
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Successfully loaded: {filename}')
            except Exception as e:
                print(f'Failed to load {filename}: {e}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    asyncio.run(main())
