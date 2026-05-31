import discord
from discord.ext import commands
import json
import os
import asyncio

# This function reads the prefix from your prefixes.json file
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
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

async def load_cogs():
    # This specifically looks inside your 'cogs' folder
    await bot.load_extension('cogs.help')

async def main():
    async with bot:
        await load_cogs()
        # This pulls your token from your GitHub/Hosting secret settings
        # You do NOT type your token here
        await bot.start(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    asyncio.run(main())
