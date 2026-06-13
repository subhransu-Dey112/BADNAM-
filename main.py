import os
import sys
import subprocess

# Force-install PyNaCl if missing
try:
    import nacl
except ImportError:
    print("⚠️ PyNaCl missing. Attempting force-install...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynacl"])

import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="b!", intents=intents, help_command=None)

@bot.event
async def setup_hook():
    print("🔄 Loading modules...")
    extensions = ["cogs.help", "cogs.recovery", "cogs.massroles", "cogs.music"]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    print(f"🚀 Bot is online as: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="b!help"))

async def main():
    keep_alive()
    token = os.environ.get("BOT_TOKEN")
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
