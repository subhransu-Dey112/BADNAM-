import discord
from discord.ext import commands

# Gen Z / Simple Language Mapping
COMMAND_MAP = {
    "🛡️ Server Guard": "I keep the server safe from bad guys. Use `b!antinuke` to turn on my shields!",
    "🔨 The Cleaners": "I take out the trash (bad messages) and ban the trolls. Use `b!ban` or `b!kick`.",
    "🎟️ Help Desk": "Need help? I open private rooms for you to talk to staff. Just use `b!ticket`.",
    "📈 My Rank": "Check how cool you are! Use `b!rank` to see your level and points.",
    "💵 Money & Fun": "Earn coins, play games, and buy stuff in the shop. Use `b!bal` or `b!slots`.",
    "🎶 Vibe Vibes": "I play your favorite music. Use `b!play` and just enjoy the tunes.",
    "🚪 The Gate": "I check if new people are real before letting them in. Use `b!verification`."
}

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=cat, description=cat.split(" ")[1] + " stuff!", emoji=cat.split(" ")[0]) 
            for cat in COMMAND_MAP.keys()
        ]
        super().__init__(placeholder="🌟 Tap here to see what I can do!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(
            title=f"{category} ✨",
            description=f"**Here’s the simple version:**\n\n{COMMAND_MAP.get(category)}",
            color=discord.Color.from_rgb(255, 105, 180) # Hot Pink Vibe
        )
        embed.set_footer(text="BADNAM: Simple, Safe, & Fun for everyone.")
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
            title="👋 Hey Bestie! Welcome to BADNAM",
            description="I’m your friendly bot helper! No matter if you're 5 or 80, I’m here to make things easy. Tap the menu below to pick what you need!",
            color=discord.Color.from_rgb(147, 112, 219) # Medium Purple
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.add_field(name="🌐 Visit Us", value="[Click for Website](https://badnam.com)", inline=True)
        embed.add_field(name="💬 Chat with us", value="[Join Support](https://discord.gg/yourlink)", inline=True)
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
