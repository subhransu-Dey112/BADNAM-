import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="b!", intents=intents) # Default prefix

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def load_extensions():
    # JUST ADD THE NAMES OF THE FILES YOU WANT TO RUN HERE
    # If you don't add them here, they won't load (this is the safe way!)
    extensions = ['cogs.help'] 
    
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f'Successfully loaded {ext}')
        except Exception as e:
            print(f'Failed to load {ext}: {e}')

async def main():
    async with bot:
        await load_extensions()
        # Ensure you have DISCORD_TOKEN in your GitHub Secrets
        await bot.start(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    asyncio.run(main())
