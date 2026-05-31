import discord
from discord.ext import commands

# Command Database
COMMANDS_DB = {
    "🛡️ SECURITY": {
        "Antinuke": "`b!setup`, `b!antinuke`, `b!panic`",
        "Automod": "`b!automod`, `b!blackwords`, `b!antispam`",
        "Quarantine": "`b!quarantine`, `b!unquarantine`",
        "Adv. Security": "`b!whois`, `b!anpanic`",
        "Enterprise Intel": "`b!proxyblocker`, `b!threatmesh`",
        "AI AutoMod": "`b!ai-mod toxicity`"
    },
    "⚙️ MANAGEMENT": {
        "Tickets": "`b!ticket`, `b!panel`",
        "Custom Roles": "`b!role add`",
        "Levels": "`b!rank`, `b!leaderboard`",
        "VC Levels": "`b!vclevel`",
        "Msg Count": "`b!msgcount`",
        "VC Count": "`b!vccount`",
        "Invite Count": "`b!invites`",
        "AutoRole": "`b!autorole`",
        "Join to Create": "`b!jtc`",
        "Logging": "`b!autologs`",
        "Verification": "`b!verify`",
        "Moderation": "`b!ban`, `b!kick`, `b!mute`",
        "Giveaway": "`b!giveaway`",
        "General": "`b!ping`, `b!info`"
    },
    "💬 MESSAGING": {
        "Sticky": "`b!sticky`",
        "Welcome": "`b!welcome`",
        "Leave": "`b!leave`",
        "Boost": "`b!boost`",
        "Auto Respond": "`b!autorespond`"
    },
    "✨ GAMES": {
        "Pfp Event": "`b!pfpevent`",
        "Slots": "`b!slots`",
        "Auto React": "`b!autoreact`",
        "Economy": "`b!bal`, `b!work`",
        "Utils": "`b!utils`"
    },
    "🎵 MUSIC": {
        "Music": "`b!play`, `b!skip`",
        "Voice": "`b!vc`"
    }
}

class ToolSelect(discord.ui.Select):
    def __init__(self, category):
        self.category = category
        options = [discord.SelectOption(label=tool) for tool in COMMANDS_DB[category].keys()]
        super().__init__(placeholder="> Select a module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        tool = self.values[0]
        cmds = COMMANDS_DB[self.category][tool]
        
        embed = discord.Embed(
            title=f"🛠️ {tool} Commands",
            description=f"**Commands:**\n{cmds}",
            color=0x2b2d31
        )
        embed.set_footer(text="powered by badnam development tm || developed and designed by subhransudey")
        await interaction.response.edit_message(embed=embed)

class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=cat, emoji=cat.split(" ")[0]) for cat in COMMANDS_DB.keys()]
        super().__init__(placeholder="> Choose a Specific Module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        
        view = discord.ui.View(timeout=180)
        view.add_item(ToolSelect(category))
        
        embed = discord.Embed(
            title=f"{category}",
            description=f"You selected **{category}**.\n\n👇 Pick a specific module below to view commands.",
            color=0x2b2d31
        )
        embed.set_footer(text="powered by badnam development tm || developed and designed by subhransudey")
        await interaction.response.edit_message(embed=embed, view=view)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(CategorySelect())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        # Calculate total commands dynamically just to be accurate
        total_cmds = sum(len(cmds.split(',')) for cats in COMMANDS_DB.values() for cmds in cats.values())

        embed = discord.Embed(
            title="Hey , I'm badnam™",
            description=(
                "A powerful multipurpose bot with Fastest Antinuke\n"
                "**My Prefix is:** `?`\n"
                f"**Total Commands:** `{total_cmds}+`\n"
                "Choose a Specific Module of your Desire\n"
                "\n.\n.\n.\n.\n.\n\n"
                "**[invite me](https://discord.com/oauth2) || [support server](https://discord.gg/yourlink) || [website](https://badnam.com)**"
            ),
            color=0x2b2d31
        )
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            
        embed.set_footer(text="powered by badnam development tm || developed and designed by subhransudey")
            
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
