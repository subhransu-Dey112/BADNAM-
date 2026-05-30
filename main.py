import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================================
# 🌐 KEEP-ALIVE SERVER (For Render)
# ==========================================================
app = Flask('')
@app.route('/')
def home(): return "⚡ BADNAM Enterprise Core Online."
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# ==========================================================
# 🤖 BOT ARCHITECTURE & COG LOADER
# ==========================================================
class BadnamBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.get_prefix_dynamic, 
            intents=discord.Intents.all(), 
            help_command=None
        )

    async def get_prefix_dynamic(self, bot, message):
        # Future: This will pull from Redis cache instantly
        return "b!"

    async def setup_hook(self):
        print("⚙️ Booting Master Core...")
        
        # Automatically load all modules from the 'cogs' folder
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"✅ Loaded Module: {filename}")
                except Exception as e:
                    print(f"❌ Failed to load {filename}: {e}")
                    
        # Sync slash commands globally
        await self.tree.sync()
        print("🌍 Global Slash Commands Synced.")

    async def on_ready(self):
        print(f"👑 BADNAM Master is online as {self.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Over 2000+ Commands"))

bot = BadnamBot()

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get('DISCORD_TOKEN'))
