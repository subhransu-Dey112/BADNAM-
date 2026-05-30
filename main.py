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
def home(): 
    return "⚡ BADNAM Enterprise Core Online."

def run(): 
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive(): 
    Thread(target=run).start()

# ==========================================================
# 🤖 BOT ARCHITECTURE & ENGINE
# ==========================================================
class BadnamBot(commands.Bot):
    def __init__(self):
        # Intents allow the bot to see members, messages, etc.
        intents = discord.Intents.all()
        
        super().__init__(
            command_prefix=self.get_dynamic_prefix, 
            intents=intents, 
            help_command=None
        )

    async def get_dynamic_prefix(self, bot, message):
        # Right now it defaults to b! 
        # Later, we will hook this up to the database so it can change per server!
        return ["b!", "B!"]

    async def setup_hook(self):
        print("⚙️ Booting Master Core...")
        
        # This automatically looks inside your "cogs" folder and loads every file
        if not os.path.exists('./cogs'):
            os.makedirs('./cogs')

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"✅ Loaded Module: {filename}")
                except Exception as e:
                    print(f"❌ Failed to load {filename}: {e}")

    async def on_ready(self):
        print(f"👑 BADNAM Master is online as {self.user}")
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="b!help | Securing Servers"
        ))

# ==========================================================
# LAUNCHER
# ==========================================================
bot = BadnamBot()

if __name__ == "__main__":
    keep_alive()
    # Grabs your token securely from Render's environment variables
    bot.run(os.environ.get('DISCORD_TOKEN'))
