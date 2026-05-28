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
# 🌐 24/7 KEEP-ALIVE SERVER
# ==========================================================
app = Flask('')
@app.route('/')
def home(): return "⚡ BADNAM Master Core Online."
def run(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): Thread(target=run).start()

# ==========================================================
# 📂 UNIVERSAL DATABASE (Prefixes, NoPrefix, Blacklist)
# ==========================================================
DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"prefixes": {}, "noprefix": [], "bl_users": [], "bl_servers": []}, f)
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except:
        return {"prefixes": {}, "noprefix": [], "bl_users": [], "bl_servers": []}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_prefix(bot, message):
    db = load_db()
    pfx = db["prefixes"].get(str(message.guild.id), "b!") if message.guild else "b!"
    if message.author.id in db["noprefix"]:
        return ["", pfx] 
    return pfx

# ==========================================================
# 🛡️ UI COMPONENTS (Verification & Help)
# ==========================================================
class VerifyButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify to Enter", style=discord.ButtonStyle.green, custom_id="verify_btn_badnam")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Verified")
        if not role:
            role = await interaction.guild.create_role(name="Verified", color=discord.Color.green(), reason="BADNAM Auto-Setup")
        
        if role in interaction.user.roles:
            await interaction.response.send_message("❌ You are already verified!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ You have been verified. Welcome to the Empire!", ephemeral=True)

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", description="Security and Anti-nuke commands", emoji="🛡️"),
            discord.SelectOption(label="Moderation", description="Purge, ban, and server management", emoji="🔨"),
            discord.SelectOption(label="General", description="Basic bot commands", emoji="🌐"),
            discord.SelectOption(label="Utility", description="Setup and configuration tools", emoji="🛠️")
        ]
        super().__init__(placeholder="Select Module From Here", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected the **{self.values[0]}** module! (Commands loading soon...)", ephemeral=True)

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpSelect())

# ==========================================================
# 🧠 BOT SETUP & BLACKLIST CHECKER
# ==========================================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)
action_tracker = defaultdict(list) 

@bot.check
async def global_blacklist_check(ctx):
    db = load_db()
    if ctx.author.id in db["bl_users"]: return False
    if ctx.guild and ctx.guild.id in db["bl_servers"]: return False
    return True

@bot.event
async def on_ready():
    print(f"👑 SUCCESS: BADNAM Engine Online as {bot.user.name}")
    bot.add_view(VerifyButton())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Over your Empire"))

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    await bot.process_commands(message)

# ==========================================================
# 👑 OWNER-ONLY SECURE COMMANDS
# ==========================================================
@bot.command(name="np")
@commands.is_owner()
async def toggle_noprefix(ctx, user: discord.User):
    db = load_db()
    if user.id in db["noprefix"]:
        db["noprefix"].remove(user.id)
        status = "REMOVED from"
    else:
        db["noprefix"].append(user.id)
        status = "ADDED to"
    save_db(db)
    await ctx.send(f"👑 **VIP Updated:** {user.mention} has been {status} the No-Prefix list.")

@bot.command(name="banuser")
@commands.is_owner()
async def ban_user(ctx, user: discord.User):
    db = load_db()
    if user.id not in db["bl_users"]:
        db["bl_users"].append(user.id)
        save_db(db)
        await ctx.send(f"🔨 **Blacklisted:** {user.mention} can no longer use BADNAM.")
    else:
        await ctx.send(f"⚠️ {user.mention} is already blacklisted.")

@bot.command(name="banserver")
@commands.is_owner()
async def ban_server(ctx, guild_id: int):
    db = load_db()
    if guild_id not in db["bl_servers"]:
        db["bl_servers"].append(guild_id)
        save_db(db)
        await ctx.send(f"🔨 **Server Blacklisted:** Server ID `{guild_id}` can no longer use BADNAM.")
    else:
        await ctx.send("⚠️ This server is already blacklisted.")

# ==========================================================
# 🛡️ MODERATION & UTILITY COMMANDS
# ==========================================================
@bot.command(name="setprefix")
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix: str):
    db = load_db()
    db["prefixes"][str(ctx.guild.id)] = new_prefix
    save_db(db)
    await ctx.send(f"✅ Success! Prefix changed to: `{new_prefix}`")

@bot.command(name="vsetup")
@commands.has_permissions(administrator=True)
async def vsetup(ctx):
    embed = discord.Embed(title="🔒 Server Verification", description="Click the button below to prove you are human.", color=0x2b2d31)
    await ctx.send(embed=embed, view=VerifyButton())
    await ctx.message.delete()

@bot.command(name="unbanall")
@commands.has_permissions(administrator=True)
async def unbanall(ctx):
    banned_users = [entry async for entry in ctx.guild.bans()]
    if not banned_users: return await ctx.send("✅ Nobody is currently banned.")
    msg = await ctx.send(f"🔄 **Mass Recovery:** Reversing {len(banned_users)} bans. Please wait...")
    count = 0
    for ban_entry in banned_users:
        try:
            await ctx.guild.unban(ban_entry.user, reason="BADNAM Mass Recovery")
            count += 1
        except: pass
    await msg.edit(content=f"✅ **Mass Recovery Complete:** Unbanned {count} users.")

@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Purged **{amount}** messages.")
    await msg.delete(delay=3)

@bot.command(name="purgeuser")
@commands.has_permissions(manage_messages=True)
async def purgeuser(ctx, member: discord.Member, amount: int):
    await ctx.message.delete()
    deleted = await ctx.channel.purge(limit=amount, check=lambda m: m.author == member)
    msg = await ctx.send(f"🧹 Purged **{len(deleted)}** messages from {member.mention}.")
    await msg.delete(delay=3)

@bot.command(name="nuke")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    channel = ctx.channel
    position = channel.position
    new_channel = await channel.clone(reason="BADNAM Nuke Command")
    await channel.delete()
    await new_channel.edit(position=position)
    await new_channel.send("https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif\n🚨 **Channel Nuked.**")

@bot.command(name="help")
async def custom_help(ctx):
    pfx = get_prefix(bot, ctx.message)
    if isinstance(pfx, list): pfx = pfx[1] 
    
    embed = discord.Embed(title="Hey , I'm Badnam", description="A powerful multipurpose bot with Fastest Antinuke", color=0x2b2d31)
    
    body_text = (
        f"• **My Prefix is** `{pfx}`\n"
        f"• **Total Commands:** `1000`\n"
        f"• **Choose a Specific Module of your Desire**\n"
        f"> 🛡️ » Antinuke\n"
        f"> 🤖 » AutoMod\n"
        f"> 🔗 » Automations\n"
        f"> 🤍 » Autoresponder\n"
        f"> 🎭 » CustomRole\n"
        f"> 🎲 » Fun\n"
        f"> 🌐 » General\n"
        f"> 🎁 » Giveaway\n"
        f"> 🏆 » Leaderboard\n"
        f"> 📜 » Logging\n"
        f"> 🔨 » Moderation\n"
        f"> 🎵 » Music\n"
        f"> 👑 » Permit\n"
        f"> 🖼️ » Pfp\n"
        f"> 🔘 » ReactionRoles\n"
        f"> 🎫 » Ticket\n"
        f"> 🛠️ » Utility\n"
        f"> 🔊 » Voice\n"
        f"> 🎙️ » VoiceMaster\n"
        f"> 👋 » Welcomer\n\n"
        f"**🔗 Links**\n"
        f"**[Invite Me](https://discord.com) | [Support Server](https://discord.gg/hxJqvcEeBC) | [Website](https://discord.com)**"
    )
    
    embed.description = body_text
    embed.set_footer(text="Powered By Badnam Development™ | Developer and owner subhransudey")
    
    await ctx.send(embed=embed, view=HelpView())

@bot.command(name="control")
@commands.has_permissions(administrator=True)
async def control(ctx):
    pfx = get_prefix(bot, ctx.message)
    if isinstance(pfx, list): pfx = pfx[1]
    embed = discord.Embed(title="🛡️ BADNAM Control Panel", description="Automated system hub.", color=0x2b2d31)
    embed.add_field(name="🟢 System Status", value="Active 24/7", inline=True)
    embed.add_field(name="⚙️ Prefix", value=f"`{pfx}`", inline=True)
    await ctx.send(embed=embed)

# ==========================================================
# 🚨 MILITARY-GRADE ANTI-NUKE PROTOCOL
# ==========================================================
@bot.event
async def on_guild_channel_delete(channel):
    guild = channel.guild
    current_time = time.time()
    async for entry in guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
        rogue_user = entry.user
        if rogue_user.id == guild.owner_id or rogue_user.id == bot.user.id: return
        
        user_logs = action_tracker[rogue_user.id]
        user_logs = [t for t in user_logs if current_time - t < 8]
        user_logs.append(current_time)
        action_tracker[rogue_user.id] = user_logs
        
        if len(user_logs) >= 2:
            try:
                member = await guild.fetch_member(rogue_user.id)
                await member.edit(roles=[], reason="BADNAM SHIELD: Nuke detected.")
                await guild.ban(rogue_user, reason="BADNAM SHIELD: Channel deletion.")
            except: pass

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get('DISCORD_TOKEN'))
