import discord
from discord.ext import commands

# Dictionary mapping categories to their commands
COMMAND_MAP = {
    "Anti-Nuke": "`b!setup` `b!antinuke` `b!quarantine` `b!panic` `b!backup` `b!sanitize`",
    "AutoMod": "`b!automod` `b!blackwords` `b!antispam` `b!antilink` `b!antiinvite`",
    "Verification": "`b!verification` `b!captcha` `b!verify` `b!joingate` `b!antiraid`",
    "Moderation": "`b!ban` `b!kick` `b!mute` `b!timeout` `b!purge` `b!lock` `b!warn`",
    "Tickets": "`b!ticket` `b!panel` `b!autothread` `b!modmail`",
    "Economy": "`b!bal` `b!work` `b!daily` `b!crime` `b!deposit` `b!withdraw` `b!shop` `b!slots`",
    "Music": "`b!play` `b!stop` `b!pause` `b!skip` `b!queue` `b!loop` `b!volume` `b!filter`",
    "Logging": "`b!autologs` `b!cases` `b!case` `b!diagnose` `b!stats`",
    # ... (You can add the rest of your modules here following this pattern)
}

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=cat, description=f"View {cat} commands", emoji="📂") for cat in COMMAND_MAP.keys()]
        super().__init__(placeholder="👉 Select a category to see commands", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(
            title=f"🛡️ {category} Module",
            description=f"**Available Commands:**\n\n{COMMAND_MAP.get(category, 'No commands listed.')}",
            color=discord.Color.from_rgb(128, 0, 128) # Professional deep purple
        )
        embed.set_footer(text="BADNAM Security & Management System")
        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(HelpSelect())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(
            title="✨ BADNAM Control Panel",
            description="Welcome, Commander. Use the dropdown menu below to navigate the system modules.",
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.add_field(name="🌐 Official Website", value="[Click here](https://badnam.com)", inline=True)
        embed.add_field(name="🔗 Support Hub", value="[Join Here](https://discord.gg/yourlink)", inline=True)
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
