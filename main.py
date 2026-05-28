import discord
from discord.ext import commands
import os
import json
import time
from collections import defaultdict
from flask import Flask
from threading import Thread

# -- 24/7 Hosting Engine --
app = Flask('')
@app.route('/')
def home(): return "⚡ BADNAM Core Online."
def run(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): Thread(target=run).start()

# -- Prefix System --
PREFIX_FILE = "prefixes.json"
def get_prefix(bot, message):
    if not message.guild: return "b!"
    try:
        with open(PREFIX_FILE, "r") as f: prefixes = json.load(f)
    except: prefixes = {}
    return prefixes.get(str(message.guild.id), "b!")

# -- Bot Setup --
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
action_tracker = defaultdict(list) 

@bot.event
async def on_ready():
    print(f"👑 SUCCESS: BADNAM Bot logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="b!control"))

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    await bot.process_commands(message)

# -- Commands --
@bot.command(name="setprefix")
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix: str):
    try:
        with open(PREFIX_FILE, "r") as f: prefixes = json.load(f)
    except: prefixes = {}
    prefixes[str(ctx.guild.id)] = new_prefix
    with open(PREFIX_FILE, "w") as f: json.dump(prefixes, f, indent=4)
    await ctx.send(f"✅ Success! Prefix changed to: `{new_prefix}`")

@bot.command(name="control")
async def control(ctx):
    pfx = get_prefix(bot, ctx.message)
    embed = discord.Embed(title="🛡️ BADNAM Control Panel", description="Easy automated system hub.", color=0x000000)
    embed.add_field(name="🟢 System Status", value="Active 24/7", inline=True)
    embed.add_field(name="⚙️ Prefix", value=f"`{pfx}` (Change via `{pfx}setprefix`)", inline=True)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get('DISCORD_TOKEN'))
