import discord
from discord.ext import commands
import json

# The complete 221-command database
COMMANDS_DB = {
    "🛡️ SECURITY": {
        "Anti-Nuke": "b!setup, b!antinuke enable/disable, b!antinuke dynamic, b!setlimit, b!quarantine, b!unquarantine, b!panic, b!unpanic, b!backup, b!trusted, b!extraowner, b!sanitize",
        "AutoMod": "b!automod enable/disable, b!blackwords, b!antispam, b!antilink, b!antiinvite, b!automod regex/zalgo",
        "Advanced Security": "b!whois, b!systempanic, b!anpanic, b!antinukelog, b!quarantinerole",
        "Protections": "b!antidelete, b!antibot, b!antiwebhook, b!trustscore, b!webhook-intercept",
        "Enterprise Intel": "b!proxyblocker, b!threatmesh, b!autoquarantine, b!overrideowner, b!bypasscheck, b!strictmode, b!rolemonitor",
        "AI AutoMod": "b!ai-mod toxicity/scam/image, b!automodlog, b!automodwhitelist"
    },
    "⚙️ MANAGEMENT": {
        "Moderation": "b!ban, b!softban, b!hackban, b!unban, b!kick, b!timeout, b!mute, b!warn, b!purge, b!lock/unlock, b!note",
        "Tickets": "b!ticket enable/close/transcript, b!panel create/button, b!autothread, b!modmail",
        "Verification": "b!verification setup, b!captcha, b!verify, b!joingate, b!antiraid, b!username-filter",
        "Recovery": "b!recoverysetup, b!verifychannel, b!oauthlink, b!pull, b!tokenrefresh, b!authusers"
    },
    "💬 MESSAGING": {
        "Essentials": "b!sticky, b!welcome, b!leave, b!boostmessage",
        "Interaction": "b!autorespond, b!autoreact, b!suggest, b!starboard",
        "Logging": "b!autologs, b!cases, b!diagnose"
    },
    "✨ GAMES": {
        "Events": "b!giveaway, b!invites, b!messagescount, b!voicecount, b!avatar, b!banner",
        "Economy": "b!balance, b!work, b!daily, b!crime, b!shop, b!slots, b!roulette, b!blackjack",
        "Utils": "b!embed, b!rr setup, b!tag, b!role, b!channel, b!poll, b!afk"
    },
    "🎵 MUSIC": {
        "Playback": "b!play, b!stop, b!pause, b!skip, b!queue, b!loop, b!volume",
        "Voice": "b!autovoice, b!vc lock/unlock/kick, b!vcrole, b!rank, b!levelconfig, b!xp"
    }
}

class ToolSelect(discord.ui.Select):
    def __init__(self, cat, main_embed):
        self.cat = cat
        self.main_embed = main_embed
        options = [discord.SelectOption(label=t) for t in COMMANDS_DB[cat].keys()]
        options.append(discord.SelectOption(label="Back", emoji="↩️"))
        super().__init__(placeholder="> Select a tool...", options=options)
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Back":
            await interaction.response.edit_message(embed=self.main_embed, view=HelpView(self.main_embed))
            return
        embed = discord.Embed(title=f"Module: {self.values[0]}", description=COMMANDS_DB[self.cat][self.values[0]], color=0x2b2d31)
        await interaction.response.edit_message(embed=embed)

class CategorySelect(discord.ui.Select):
    def __init__(self, main_embed):
        self.main_embed = main_embed
        options = [discord.SelectOption(label=cat, emoji=cat.split(" ")[0]) for cat in COMMANDS_DB.keys()]
        super().__init__(placeholder="> Choose a module...", options=options)
    async def callback(self, interaction: discord.Interaction):
        view = discord.ui.View(timeout=180).add_item(ToolSelect(self.values[0], self.main_embed))
        embed = discord.Embed(title=f"Category: {self.values[0]}", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=view)

class HelpView(discord.ui.View):
    def __init__(self, main_embed):
        super().__init__(timeout=180)
        self.add_item(CategorySelect(main_embed))

class Help(commands.Cog):
    def __init__(self, bot): self.bot = bot
    
    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(title="BADNAM™ Help", description="[Invite](https://discord.com/oauth2/authorize?client_id=1509404143712993441&permissions=8&integration_type=0&scope=bot+applications.commands) | [Support](https://discord.gg/hxJqvcEeBC)", color=0x2b2d31)
        await ctx.send(embed=embed, view=HelpView(embed))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f"Prefix changed to `{prefix}`")

async def setup(bot): await bot.add_cog(Help(bot))
