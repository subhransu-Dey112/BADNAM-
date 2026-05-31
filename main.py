import discord
from discord.ext import commands
import json
import os
import asyncio

# Setup prefix system
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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

async def load_extensions():
    # Automatically finds and loads every .py file in your 'cogs' folder
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
        # This pulls the token from your GitHub Secrets
        await bot.start(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    asyncio.run(main())
