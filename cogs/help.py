import discord
from discord.ext import commands

# The complete 221-command database mapped to the select menu options
COMMANDS_DB = {
    "sec": {
        "title": "🛡️ Security Commands",
        "text": "**Anti-Nuke:** b!setup, b!antinuke enable/disable, b!antinuke dynamic, b!setlimit, b!quarantine, b!unquarantine, b!panic, b!unpanic, b!backup, b!trusted, b!extraowner, b!sanitize\n**AutoMod:** b!automod enable/disable, b!blackwords, b!antispam, b!antilink, b!antiinvite, b!automod regex/zalgo\n**Advanced Security:** b!whois, b!systempanic, b!anpanic, b!antinukelog, b!quarantinerole\n**Protections:** b!antidelete, b!antibot, b!antiwebhook, b!trustscore, b!webhook-intercept\n**AI AutoMod:** b!ai-mod toxicity/scam/image, b!automodlog, b!automodwhitelist"
    },
    "man": {
        "title": "⚙️ Management Commands",
        "text": "**Moderation:** b!ban, b!softban, b!hackban, b!unban, b!kick, b!timeout, b!mute, b!warn, b!purge, b!lock/unlock, b!note\n**Tickets:** b!ticket enable/close/transcript, b!panel create/button, b!autothread, b!modmail\n**Verification:** b!verification setup, b!captcha, b!verify, b!joingate, b!antiraid, b!username-filter\n**Recovery:** b!recoverysetup, b!verifychannel, b!oauthlink, b!pull, b!tokenrefresh, b!authusers"
    },
    "msg": {
        "title": "💬 Messaging Commands",
        "text": "**Essentials:** b!sticky, b!welcome, b!leave, b!boostmessage\n**Interaction:** b!autorespond, b!autoreact, b!suggest, b!starboard\n**Logging:** b!autologs, b!cases, b!diagnose"
    },
    "gam": {
        "title": "✨ Games & Utils",
        "text": "**Events:** b!giveaway, b!invites, b!messagescount, b!voicecount, b!avatar, b!banner\n**Economy:** b!balance, b!work, b!daily, b!crime, b!shop, b!slots, b!roulette, b!blackjack\n**Utils:** b!embed, b!rr setup, b!tag, b!role, b!channel, b!poll, b!afk"
    },
    "mus": {
        "title": "🎵 Music & Voice",
        "text": "**Playback:** b!play, b!stop, b!pause, b!skip, b!queue, b!loop, b!volume\n**Voice:** b!autovoice, b!vc lock/unlock/kick, b!vcrole, b!rank, b!levelconfig, b!xp"
    }
}

class HelpDropdown(discord.ui.Select):
    def __init__(self, main_embed):
        self.main_embed = main_embed
        options = [
            discord.SelectOption(label="Security", value="sec", emoji="🛡️"),
            discord.SelectOption(label="Management", value="man", emoji="⚙️"),
            discord.SelectOption(label="Messaging", value="msg", emoji="💬"),
            discord.SelectOption(label="Games", value="gam", emoji="✨"),
            discord.SelectOption(label="Music", value="mus", emoji="🎵"),
            discord.SelectOption(label="Main Menu", value="main", emoji="↩️")
        ]
        super().__init__(placeholder="> Choose a Specific Module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # If user selects Main Menu, return to original embed
        if self.values[0] == "main":
            await interaction.response.edit_message(embed=self.main_embed)
            return

        # Load specific category details
        data = COMMANDS_DB[self.values[0]]
        embed = discord.Embed(
            title=data["title"],
            description=data["text"],
            color=0x2b2d31
        )
        
        # Keep the styling elements matching the original theme
        if interaction.client.user.avatar:
            embed.set_thumbnail(url=interaction.client.user.avatar.url)
        embed.set_footer(
            text="Powered by BADNAM Development™ | Developed and designed by subhransudey", 
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )
        
        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self, main_embed):
        super().__init__(timeout=180)
        self.add_item(HelpDropdown(main_embed))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        # Fetch prefix dynamically or use default
        prefix = ctx.prefix

        embed = discord.Embed(
            title="Hey, I'm BADNAM™",
            description=(
                f"A powerful multipurpose bot with the fastest Antinuke.\n"
                f"**My Prefix is:** `{prefix}`\n"
                f"**Total Commands:** `221+`\n\n"
                f"**Choose a Specific Module of your Desire:**\n"
                f"🛡️ Security\n"
                f"⚙️ Management\n"
                f"💬 Messaging\n"
                f"✨ Games\n"
                f"🎵 Music\n\n"
                f"[Invite Me](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot) | "
                f"[Support Server](https://discord.gg/hxJqvcEeBC) | "
                f"[Website](https://badnam-1.onrender.com)"
            ),
            color=0x2b2d31
        )

        # Automatically display your bot's avatar thumbnail dynamically
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_footer(
            text="Powered by BADNAM Development™ | Developed and designed by subhransudey",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )

        await ctx.send(embed=embed, view=HelpView(embed))

async def setup(bot):
    await bot.add_cog(Help(bot))
