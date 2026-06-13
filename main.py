import discord
from discord.ext import commands
import os
import asyncio
import sys

# Pre-flight check to debug why libraries are not loading
try:
    import nacl
    print(f"✅ PyNaCl found at: {nacl.__file__}")
except ImportError:
    print("❌ CRITICAL: PyNaCl is not installed or importable.")

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
            # This will show the exact line number where the music cog fails
            import traceback
            traceback.print_exc()

@bot.event
async def on_ready():
    print(f"🚀 Bot is online as: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="b!help"))

async def main():
    keep_alive()
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("❌ ERROR: BOT_TOKEN is missing!")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
