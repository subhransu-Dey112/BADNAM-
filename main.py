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
def home(): return "⚡ BADNAM Elite Master Core Online."
def run(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): Thread(target=run).start()

# ==========================================================
# 📂 UNIVERSAL DATABASE
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
# 💎 PREMIUM UI ARCHITECTURE
# ==========================================================
class VerifyButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify Securely", style=discord.ButtonStyle.green, custom_id="verify_btn_badnam", emoji="🛡️")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name="Verified")
        if not role:
            role = await interaction.guild.create_role(name="Verified", color=discord.Color.green(), reason="BADNAM Auto-Setup")
        
        if role in interaction.user.roles:
            await interaction.response.send_message("❌ You are already verified.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("💎 **Verification Successful.** Welcome to the Elite Empire!", ephemeral=True)

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Antinuke", emoji="🛡️", value="antinuke"),
            discord.SelectOption(label="AutoMod", emoji="🤖", value="automod"),
            discord.SelectOption(label="Automations", emoji="🔗", value="automations"),
            discord.SelectOption(label="AutoResponder", emoji="🤍", value="autoresponder"),
            discord.SelectOption(label="Custom Roles", emoji="🎭", value="customroles"),
            discord.SelectOption(label="Dating", emoji="💖", value="dating"),
            discord.SelectOption(label="Fun & Games", emoji="🎲", value="fun"),
            discord.SelectOption(label="General", emoji="🌐", value="general"),
            discord.SelectOption(label="Giveaways", emoji="🎁", value="giveaways"),
            discord.SelectOption(label="Leaderboard", emoji="🏆", value="leaderboard"),
            discord.SelectOption(label="Logging", emoji="📜", value="logging"),
            discord.SelectOption(label="Moderation", emoji="🔨", value="moderation"),
            discord.SelectOption(label="Music", emoji="🎵", value="music"),
            discord.SelectOption(label="Permit System", emoji="👑", value="permit"),
            discord.SelectOption(label="Pfp", emoji="🖼️", value="pfp"),
            discord.SelectOption(label="Reaction Roles", emoji="🔘", value="reactionroles"),
            discord.SelectOption(label="Ticketing", emoji="🎫", value="ticketing"),
            discord.SelectOption(label="Utility", emoji="🛠️", value="utility"),
            discord.SelectOption(label="Vanity Roles", emoji="✨", value="vanityroles"),
            discord.SelectOption(label="Voice", emoji="🔊", value="voice"),
            discord.SelectOption(label="VoiceMaster", emoji="🎙️", value="voicemaster"),
            discord.SelectOption(label="Welcomer", emoji="👋", value="welcomer")
        ]
        super().__init__(placeholder="💎 Select Module From Here", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        embed = discord.Embed(color=0x2b2d31)
        
        data = {
            "antinuke": ("🛡️ Advanced Antinuke Protection", "An iron wall between your server and destructive nukers. Protect your server from unauthorized changes. Auto-detection for bans, kicks, role updates, and channel deletion. Lightning-fast detection and instant countermeasures ensure no threat ever gets past BADNAM."),
            "automod": ("🤖 Intelligent AutoMod", "Intelligent automation that filters spam, bad words, invites, caps, toxicity, and rule-breakers in real time. Keep your chat spotless without lifting a finger."),
            "automations": ("🔗 Automations", "Automate repetitive server tasks with fully customizable triggers and actions so your server runs like a well-oiled machine, 24/7."),
            "autoresponder": ("🤍 AutoResponder", "Set up smart, instant replies to common triggers and keywords. Set up custom triggers and responses to automate FAQs. BADNAM responds so you don’t have to."),
            "customroles": ("🎭 Custom Roles", "Create, manage, and assign roles with pinpoint precision tailored exactly the way you want them."),
            "dating": ("💖 Dating", "Spark real connections within your community through interactive dating and profile features built for engagement."),
            "fun": ("🎲 Fun & Games", "A massive arsenal of games, challenges, and entertainment commands. Boredom doesn’t stand a chance."),
            "general": ("🌐 General Commands", "All the essential tools you need for smooth and seamless everyday server interaction right at your fingertips."),
            "giveaways": ("🎁 Giveaways & Events", "Run flawless giveaways with requirements, rerolls, winner selection, automated ending systems, and logging making every event truly memorable."),
            "leaderboard": ("🏆 Leaderboard", "Track activity and rank members server-wide turning engagement into an exciting ongoing competition."),
            "logging": ("📜 Logging", "Razor-sharp detailed logs of every server event giving you complete visibility and total oversight at all times."),
            "moderation": ("🔨 Powerful Moderation", "A powerhouse suite of 60+ commands for serious community management. Comprehensive moderation suite with logs, case management, strict punishment systems, and warnings handled with surgical precision."),
            "music": ("🎵 High Quality Music", "Crystal-clear high-fidelity music playback with seamless queue management and lag-free streaming. Supports filters, playlists, and custom volume controls. Let BADNAM set the perfect vibe."),
            "permit": ("👑 Permit System", "Granular role-based permission control like never before putting the right power in the right hands always."),
            "pfp": ("🖼️ Profile Pictures (Pfp)", "Let members showcase and manage their avatars and social profiles effortlessly within the server."),
            "reactionroles": ("🔘 Reaction Roles", "Self-role assignment with a single reaction. Fast, clean, and completely effortless for every member."),
            "ticketing": ("🎫 Ticketing System", "Organize support with advanced panels, transcripts, internal logging, and customizable categories built for servers that mean business."),
            "utility": ("🛠️ Utility", "A Swiss Army knife of server tools. From detailed info to powerful management utilities all in one place."),
            "vanityroles": ("✨ Vanity Roles", "Add a touch of personality and flair to every member’s profile with a sleek vanity role system."),
            "voice": ("🔊 Voice", "Advanced voice channel management tools keeping your audio spaces organized, controlled, and always in check."),
            "voicemaster": ("🎙️ VoiceMaster (Join to Create)", "The ultimate Join-to-Create system. Dynamic voice channels that create themselves when you join and delete when you leave. Members spin up their own temporary voice channels instantly."),
            "welcomer": ("👋 Welcomer", "Greet new members with stunning fully customizable welcome and leave messages, image cards, dynamic variables, and role assignments making every arrival unforgettable.")
        }

        embed.title, embed.description = data.get(selected, ("Error", "Module data not found."))
        embed.set_footer(text="Powered By Badnam Development™")
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
    if ctx.guild and ctx.guild.id in db["bl_servers"]: return False
    return True

@bot.event
async def on_ready():
    print(f"👑 SUCCESS: BADNAM Premium Engine Active as {bot.user.name}")
    bot.add_view(VerifyButton())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Over 2000+ Commands | b!help"))

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

# ==========================================================
# 🛡️ CORE EXECUTIONS
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
    embed = discord.Embed(title="🛡️ Server Verification", description="To access all channels, click the verification button below.", color=0x2b2d31)
    await ctx.send(embed=embed, view=VerifyButton())
    await ctx.message.delete()

@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Purged **{amount}** messages.")
    await msg.delete(delay=3)

@bot.command(name="nuke")
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    channel = ctx.channel
    position = channel.position
    new_channel = await channel.clone(reason="BADNAM Premium Engine Nuke")
    await channel.delete()
    await new_channel.edit(position=position)
    await new_channel.send("🚨 **Channel reset successfully.**")

@bot.command(name="help")
async def custom_help(ctx):
    pfx = get_prefix(bot, ctx.message)
    if isinstance(pfx, list): pfx = pfx[1] 
    
    embed = discord.Embed(
        title="Hey , I'm Badnam", 
        description="A powerful multipurpose bot with Fastest Antinuke", 
        color=0x2b2d31
    )
    
    categories_text = (
        "> 🛡️ » Antinuke\n> 🤖 » AutoMod\n> 🔗 » Automations\n> 🤍 » Autoresponder\n> 🎭 » Custom Roles\n> 💖 » Dating\n> 🎲 » Fun\n> 🌐 » General\n"
        "> 🎁 » Giveaways\n> 🏆 » Leaderboard\n> 📜 » Logging\n> 🔨 » Moderation\n> 🎵 » Music\n> 👑 » Permit\n> 🖼️ » Pfp\n> 🔘 » Reaction Roles\n"
        "> 🎫 » Ticketing\n> 🛠️ » Utility\n> ✨ » Vanity Roles\n> 🔊 » Voice\n> 🎙️ » VoiceMaster\n> 👋 » Welcomer"
    )

    body_text = (
        f"• **My Prefix is** `{pfx}`\n"
        f"• **Total Commands:** `2007`\n"
        f"• **Choose a Specific Module of your Desire**\n"
        f"{categories_text}\n\n"
        f"**🔗 Links**\n"
        f"**[Invite Me](https://discord.com) | [Support Server](https://discord.gg/hxJqvcEeBC) | [Website](https://discord.com)**"
    )
    
    embed.description = body_text
    embed.set_footer(text="Powered By Badnam Development™ | Developer and owner subhransudey")
    await ctx.send(embed=embed, view=HelpView())

# ==========================================================
# 🚨 ANTI-NUKE DETECTOR
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
                await member.edit(roles=[], reason="BADNAM SHIELD: Mass deletion detected.")
                await guild.ban(rogue_user, reason="BADNAM SHIELD: Automated ban.")
            except: pass

if __name__ == "__main__":
    keep_alive()
    bot.run(os.environ.get('DISCORD_TOKEN'))
