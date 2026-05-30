import discord
from discord.ext import commands

# 1. THE DATA STRUCTURE: Categories > Tools > Commands
COMMANDS_DB = {
    "🛡️ SECURITY": {
        "Antinuke": "`b!setup`, `b!antinuke`, `b!panic`",
        "Automod": "`b!blackwords`, `b!antispam`, `b!antilink`",
        "Quarantine": "`b!quarantine`, `b!unquarantine`",
        "Adv. Security": "`b!whois`, `b!anpanic`",
        "Enterprise Intel": "`b!proxyblocker`, `b!threatmesh`",
        "AI AutoMod": "`b!ai-mod toxicity`, `b!ai-mod scam`"
    },
    "⚙️ MANAGEMENT": {
        "Tickets": "`b!ticket`, `b!panel`",
        "Custom Roles": "`b!role add`",
        "Verification": "`b!verify`, `b!joingate`",
        "Moderation": "`b!ban`, `b!kick`, `b!mute`",
        "Logging": "`b!autologs`, `b!diagnose`"
        # ... (Add others here)
    }
}

class ToolSelect(discord.ui.Select):
    def __init__(self, tools_dict):
        options = [discord.SelectOption(label=tool, description=cmd) for tool, cmd in tools_dict.items()]
        super().__init__(placeholder="👉 Choose a tool to see commands", options=options)

    async def callback(self, interaction: discord.Interaction):
        tool = self.values[0]
        embed = interaction.message.embeds[0]
        embed.title = f"🛠️ {tool} Commands"
        embed.description = f"**Usage:** {self.options[0].description}" # simplified
        await interaction.response.edit_message(embed=embed)

class CategorySelect(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label=cat, emoji=cat.split(" ")[0]) for cat in COMMANDS_DB.keys()]
        super().__init__(placeholder="> Select a category to start...", options=options)

    async def callback(self, interaction: discord.Interaction):
        cat = self.values[0]
        view = discord.ui.View()
        view.add_item(ToolSelect(COMMANDS_DB[cat]))
        
        embed = discord.Embed(title=f"📦 {cat} Tools", description="Now pick a specific tool from the dropdown below:", color=0x5865F2)
        await interaction.response.edit_message(embed=embed, view=view)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(
            title="BADNAM Command Center",
            description="A powerful security & management bot built for complete Discord protection.\n\nSelect a **Category** below to see the **Tools** inside.",
            color=0x2b2d31
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed, view=discord.ui.View().add_item(CategorySelect()))

async def setup(bot):
    await bot.add_cog(Help(bot))
