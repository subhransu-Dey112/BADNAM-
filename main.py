import discord
from discord.ext import commands
import os
import asyncio
from flask import Flask
from threading import Thread

# 1. Setup Intents
intents = discord.Intents.all()

# 2. Initialize the Bot
bot = commands.Bot(command_prefix="b!", intents=intents, help_command=None)

# 3. Web Server Patch (To fix the "No open ports detected" error from image_5be95e.png)
app = Flask('')

@app.route('/')
def home():
    return "BADNAM Bot is alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Start the web server in a background thread
Thread(target=run_web_server).start()

# 4. Master List of All Loaded Modules (Cogs)
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

# 5. Boot Sequence
@bot.event
async def on_ready():
    print("========================================")
    print(f"✅ SYSTEM ONLINE: {bot.user.name} is fully armed!")
    print(f"🤖 Loaded {len(bot.cogs)} master modules successfully.")
    print("========================================")
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="over the server | b!help"
        )
    )

# 6. Async Execution
async def main():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"⚙️ Loaded: {extension}")
        except Exception as e:
            print(f"❌ Failed to load {extension}: {e}")

    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("🛑 CRITICAL ERROR: DISCORD_TOKEN environment variable not found!")
        return

    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
