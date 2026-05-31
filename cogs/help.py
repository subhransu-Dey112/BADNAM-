import discord
from discord.ext import commands

# The database of all your commands
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
        # Grabs the specific tools for whatever category was clicked
        options = [discord.SelectOption(label=tool) for tool in COMMANDS_DB[category].keys()]
        super().__init__(placeholder=f"> Select a tool...", options=options)

    async def callback(self, interaction: discord.Interaction):
        tool = self.values[0]
        cmds = COMMANDS_DB[self.category][tool]
        
        embed = discord.Embed(
            title=f"🛠️ {tool} Commands",
            description=f"**Here are the commands you can use:**\n\n{cmds}",
            color=0xffcc00
        )
        # Keeps the dropdown there so they can look at other tools!
        await interaction.response.edit_message(embed=embed)

class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=cat, emoji=cat.split(" ")[0]) for cat in COMMANDS_DB.keys()]
        super().__init__(placeholder="> Select a Category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        
        # Swaps out the main dropdown for the new tool dropdown
        view = discord.ui.View(timeout=180)
        view.add_item(ToolSelect(category))
        
        embed = discord.Embed(
            title=f"{category} Tools",
            description=f"You opened the **{category}** menu.\n\n👇 Now select a specific tool below to see its commands!",
            color=0xffcc00
        )
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
        embed = discord.Embed(
            title="BADNAM Command Center",
            description="**My Prefix:** `b!`\n\n👇 Use the dropdown menu below to select a category (Security, Management, etc.) to get started.",
            color=0xffcc00
        )
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
