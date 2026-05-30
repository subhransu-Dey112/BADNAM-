import discord
from discord.ext import commands

# 5 Categories mapping
CATEGORIES = {
    "🛡️ SECURITY": ["Antinuke", "Automod", "Quarantine", "Adv. Security", "Enterprise Intel", "AI AutoMod"],
    "⚙️ MANAGEMENT": ["Tickets", "Custom Roles", "Levels", "VC Levels", "Message Count", "VC Count", "Invite Count", "AutoRole", "Join to Create", "Logging", "Verification", "Moderation", "Giveaway", "General"],
    "💬 MESSAGING": ["Sticky Messages", "Welcome", "Leave", "Boost", "Auto Respond"],
    "✨ GAMES": ["Pfp Event", "Slots", "Auto React", "Economy", "Utilities"],
    "🎵 MUSIC": ["Music Playback", "Voice Utilities"]
}

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=cat, description=f"View {cat} settings", emoji=cat.split(" ")[0]) for cat in CATEGORIES]
        super().__init__(placeholder="> Select a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(title=f"{category} Commands", color=0x2b2d31)
        # Display commands in a clean list
        commands_list = "\n".join([f"🔸 {cmd}" for cmd in CATEGORIES[category]])
        embed.description = commands_list
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
            title=f"Hey @{ctx.author.name}",
            description=f"I am **{self.bot.user.name}**\nA powerful security & management bot built for complete Discord protection.\n\n**My Prefix:** `b!`",
            color=0x2b2d31
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        # Displaying the 5 categories
        for cat, cmds in CATEGORIES.items():
            embed.add_field(name=f"#{cat}", value=f"{len(cmds)} tools available", inline=False)

        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
