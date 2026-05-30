import discord
from discord.ext import commands
import os
import asyncio

# 1. Setup Intents (Required for Moderation, Members, and Message Content)
intents = discord.Intents.all()

# 2. Initialize the Bot
# help_command=None completely removes Discord's default help command so our custom dropdown works.
bot = commands.Bot(command_prefix="b!", intents=intents, help_command=None)

# 3. Master List of All Loaded Modules (Cogs)
initial_extensions = [
    "cogs.antinuke",
    "cogs.automod",
    "cogs.verification",
    "cogs.moderation",
    "cogs.tickets",
    "cogs.advanced_security",
    "cogs.ai_automod",
    "cogs.welcome",
    "cogs.protections",
    "cogs.enterprise",
    "cogs.utilities",
    "cogs.advanced_leveling",
    "cogs.economy",
    "cogs.logging",
    "cogs.music",
    "cogs.voice",
    "cogs.events",
    "cogs.recovery",
    "cogs.automations",
    "cogs.counters",
    "cogs.help"
]

# 4. Boot Sequence
@bot.event
async def on_ready():
    print("========================================")
    print(f"✅ SYSTEM ONLINE: {bot.user.name} is fully armed!")
    print(f"🤖 Loaded {len(bot.cogs)} master modules successfully.")
    print("========================================")
    
    # Set the bot's status message
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="over the server | b!help"
        )
    )

# 5. Async Loading and Execution
async def main():
    # Load all cogs dynamically
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"⚙️ Loaded: {extension}")
        except Exception as e:
            print(f"❌ Failed to load {extension}: {e}")

    # Fetch token from environment variables (vital for Render/Hosting security)
    # Make sure your environment variable on Render is named exactly "DISCORD_TOKEN"
    token = os.environ.get("DISCORD_TOKEN")
    
    if not token:
        print("🛑 CRITICAL ERROR: DISCORD_TOKEN environment variable not found!")
        return

    # Ignite the bot
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
