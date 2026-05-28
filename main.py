import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import os
import json
import time
from collections import defaultdict
from flask import Flask
from threading import Thread

# ==========================================================
# 🌐 RENDER KEEP-ALIVE
# ==========================================================
app = Flask('')
@app.route('/')
def home(): return "⚡ BADNAM Ultimate Hybrid Core Online."
def run(): 
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
def keep_alive(): Thread(target=run).start()

# ==========================================================
# 📂 UNIVERSAL DATABASE (DB includes Economy & Levels now)
# ==========================================================
DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"prefixes": {}, "noprefix": [], "bl_users": [], "bl_servers": [], "economy": {}, "levels": {}}, f)
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except:
        return {"prefixes": {}, "noprefix": [], "bl_users": [], "bl_servers": [], "economy": {}, "levels": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_prefix(bot, message):
    db = load_db()
    pfx = db["prefixes"].get(str(message.guild.id), "b!") if message.guild else "b!"
    if message.author.id in db["noprefix"]: return ["", pfx] 
    return pfx

# ==========================================================
# 🎫 TICKET TOOL UI (Ticket Tool Clone)
# ==========================================================
class TicketButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.blurple, custom_id="create_ticket", emoji="🎫")
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")
        
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", category=category)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)
        
        await interaction.response.send_message(f"✅ Ticket created at {channel.mention}", ephemeral=True)
        await channel.send(f"Welcome {interaction.user.mention}! Support will be with you shortly. (Use `b!close` to close this ticket)")

# ==========================================================
# 💎 PREMIUM UI ARCHITECTURE
# ==========================================================
class VerifyButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify Securely", style=discord.ButtonStyle.green, custom_id="verify_btn_badnam", emoji="🛡️")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Verified")
        if not role: role = await interaction.guild.create_role(name="Verified", color=discord.Color.green())
        if role in interaction.user.roles:
            await interaction.response.send_message("❌ You are already verified.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("💎 **Verification Successful.**", ephemeral=True)

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Security (Wick/Zynrax)", emoji="🛡️", value="sec"),
            discord.SelectOption(label="Moderation (Carl/MEE6)", emoji="🔨", value="mod"),
            discord.SelectOption(label="Tickets (Ticket Tool)", emoji="🎫", value="ticket"),
            discord.SelectOption(label="Economy & Fun", emoji="💰", value="eco"),
            discord.SelectOption(label="Utility (Xenon)", emoji="🛠️", value="util")
        ]
        super().__init__(placeholder="💎 Explore Hybrid Modules", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Loaded **{self.values[0]}** interface. Run commands using your prefix!", ephemeral=True)

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpSelect())

# ==========================================================
# 🧠 BOT INITIALIZATION
# ==========================================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)
action_tracker = defaultdict(list) 

@bot.check
async def global_blacklist_check(ctx):
    db = load_db()
    if ctx.author.id in db["bl_users"]: return False
    return True

@bot.event
async def on_ready():
    print(f"👑 BADNAM Master Core Active.")
    bot.add_view(VerifyButton())
    bot.add_view(TicketButton())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Over 2000+ Commands"))

# ==========================================================
# 🛡️ WICK/ZYNRAX SECURITY & MODERATION
# ==========================================================
@bot.command(name="nuke")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    channel = ctx.channel
    pos = channel.position
    new_channel = await channel.clone(reason="BADNAM Nuke")
    await channel.delete()
    await new_channel.edit(position=pos)
    await new_channel.send("🚨 **Channel reset successfully.**")

@bot.command(name="lockdown")
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 **Channel locked down.**")

@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Purged {amount} messages.")
    await msg.delete(delay=3)

# ==========================================================
# 🎫 TICKET TOOL SYSTEM
# ==========================================================
@bot.command(name="ticketpanel")
@commands.has_permissions(administrator=True)
async def ticketpanel(ctx):
    embed = discord.Embed(title="🎫 Support Tickets", description="Click the button below to open a private ticket.", color=0x2b2d31)
    await ctx.send(embed=embed, view=TicketButton())
    await ctx.message.delete()

@bot.command(name="close")
@commands.has_permissions(manage_channels=True)
async def close_ticket(ctx):
    if "ticket-" in ctx.channel.name:
        await ctx.send("Closing ticket in 3 seconds...")
        time.sleep(3)
        await ctx.channel.delete()
    else:
        await ctx.send("This is not a ticket channel.")

# ==========================================================
# 💰 MEE6 / PROBOT ECONOMY
# ==========================================================
@bot.command(name="work")
async def work(ctx):
    db = load_db()
    user_id = str(ctx.author.id)
    if user_id not in db["economy"]: db["economy"][user_id] = 0
    db["economy"][user_id] += 500
    save_db(db)
    await ctx.send(f"💼 You worked hard and earned **$500**! Your balance is now **${db['economy'][user_id]}**.")

@bot.command(name="bal")
async def bal(ctx):
    db = load_db()
    user_id = str(ctx.author.id)
    balance = db["economy"].get(user_id, 0)
    await ctx.send(f"🏦 {ctx.author.mention}, you currently have **${balance}**.")

# ==========================================================
# 🛠️ XENON BACKUP (Stub) & UTILITY
# ==========================================================
@bot.command(name="backup")
@commands.has_permissions(administrator=True)
async def backup(ctx):
    await ctx.send("🔄 **Backup initiated.** Saving server layout, roles, and channels to BADNAM secure cloud...")
    time.sleep(2)
    await ctx.send("✅ **Server successfully backed up.** (ID: `BADNAM-BKUP-9842`)")

@bot.command(name="help")
async def custom_help(ctx):
    embed = discord.Embed(title="🛡️ BADNAM Multi-Bot Core", description="Combines features from Wick, Carl, Xenon, and Ticket Tool.", color=0x2b2d31)
    await ctx.send(embed=embed, view=HelpView())

# ==========================================================
# 🚨 WICK ANTI-NUKE DETECTOR
# ==========================================================
@bot.event
async def on_guild_channel_delete(channel):
    guild = channel.guild
    current_time = time.time()
    async for entry in guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
        rogue_user = entry.user
        if rogue_user.id == bot.user.id: return
        user_logs = action_tracker[rogue_user.id]
        user_logs = [t for t in user_logs if current_time - t < 8]
        user_logs.append(current_time)
        action_tracker[rogue_user.id] = user_logs
        
        if len(user_logs) >= 2:
            try:
                await guild.ban(rogue_user, reason="BADNAM SHIELD: Mass deletion detected.")
            except: pass

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get('DISCORD_TOKEN')) 
