import discord
from discord.ext import commands
import os
import asyncio
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
    print(f"🚀 Bot is officially online as: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="b!help"))

# 🚨 DIAGNOSTIC: Tracks why commands are failing
@bot.event
async def on_command_error(ctx, error):
    print(f"❌ Command Error triggered by {ctx.author} on command '{ctx.command}': {error}")
    try:
        await ctx.send(f"⚠️ **An error occurred:** `{error}`")
    except:
        pass

async def main():
    keep_alive()
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("❌ CRITICAL ERROR: BOT_TOKEN is missing from environment variables!")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
