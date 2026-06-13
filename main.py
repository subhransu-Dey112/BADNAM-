import discord
from discord.ext import commands
import os
import asyncio

# Import the verification web server we built
from keep_alive import keep_alive

# Enable all intents (CRITICAL: Required for member pulling, roles, and message reading)
intents = discord.Intents.all()

# Initialize the bot with your custom prefix
# We set help_command=None because we built our own interactive help menu!
bot = commands.Bot(command_prefix="b!", intents=intents, help_command=None)

# The Setup Hook: This loads all your custom modules when the bot boots up
@bot.event
async def setup_hook():
    print("🔄 Loading modules...")
    
    # List of all your cogs
    initial_extensions = [
        "cogs.help",
        "cogs.recovery",
        "cogs.massroles",
        "cogs.music"
    ]
    
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"✅ Loaded {extension}")
        except Exception as e:
            print(f"❌ Failed to load {extension}: {e}")

# Boot up sequence
@bot.event
async def on_ready():
    print("=================================")
    print(f"🚀 Bot is online as: {bot.user.name}")
    print(f"🆔 Client ID: {bot.user.id}")
    print("=================================")
    
    # Set the bot's custom status
    await bot.change_presence(
        status=discord.Status.online, 
        activity=discord.Activity(type=discord.ActivityType.listening, name="b!help | Protecting BADNAM")
    )

# Main execution loop
async def main():
    # 1. Start the background Flask web server for the verification portal
    keep_alive()
    
    # 2. Get the Discord token from Render's Environment Variables
    token = os.environ.get("BOT_TOKEN")
    
    if not token:
        print("❌ ERROR: BOT_TOKEN is missing! Please add it to your Render Environment Variables.")
        return

    # 3. Start the Discord bot
    async with bot:
        await bot.start(token)

# Run the async loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot shut down manually.")
