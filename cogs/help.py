import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Anti-Nuke", description="Core server protection", emoji="🛡️"),
            discord.SelectOption(label="AutoMod", description="Chat filters and spam protection", emoji="🤖"),
            discord.SelectOption(label="Verification", description="Join gate and captcha", emoji="🚪"),
            discord.SelectOption(label="Moderation", description="Bans, kicks, mutes, and purges", emoji="🔨"),
            discord.SelectOption(label="Tickets", description="Support panels and modmail", emoji="🎫"),
            discord.SelectOption(label="Advanced Security", description="Deep profiling and panics", emoji="🕵️"),
            discord.SelectOption(label="AI AutoMod", description="Smart toxicity and scam filters", emoji="🧠"),
            discord.SelectOption(label="Welcome", description="Join/leave cards and autoroles", emoji="👋"),
            discord.SelectOption(label="Protections", description="Anti-delete and anti-bot", emoji="♻️"),
            discord.SelectOption(label="Enterprise", description="VPN blockers and vanity locks", emoji="🌐"),
            discord.SelectOption(label="Utilities", description="Embeds, tags, and polls", emoji="⚙️"),
            discord.SelectOption(label="Leveling", description="XP tracking and rewards", emoji="📈"),
            discord.SelectOption(label="Economy", description="Currency, shop, and gambling", emoji="💵"),
            discord.SelectOption(label="Logging", description="Audit trails and diagnostics", emoji="📂"),
            discord.SelectOption(label="Music", description="Audio playback and filters", emoji="🎵"),
            discord.SelectOption(label="Voice", description="Join-to-create and VC tools", emoji="🔊"),
            discord.SelectOption(label="Events", description="Giveaways and starboards", emoji="🎉"),
            discord.SelectOption(label="Recovery", description="OAuth member restoration", emoji="🧲"),
            discord.SelectOption(label="Automations", description="Auto-reacts and sticky messages", emoji="📌"),
            discord.SelectOption(label="Counters", description="Message and voice tracking", emoji="📊")
        ]
        super().__init__(placeholder="Select a module to view commands...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"{self.values[0]} Commands",
            description=f"Here are the commands for the **{self.values[0]}** module.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Use b!help <command> for more info.")
        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(HelpSelect())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(
            title="BADNAM Master Command Center",
            description="Welcome to BADNAM. Select a category from the dropdown below to view its commands.",
            color=discord.Color.dark_theme()
        )
        
        # Bot & Developer Info
        embed.add_field(name="👑 Developer", value="YourNameHere", inline=True)
        embed.add_field(name="🔗 Support Server", value="[Join Here](https://discord.gg/yourlink)", inline=True)
        embed.add_field(name="🌐 Website", value="[badnam.com](https://badnam.com)", inline=True)
        
        # Showcase the 20 modules
        modules_list = (
            "`Anti-Nuke` `AutoMod` `Verification` `Moderation` `Tickets`\n"
            "`Advanced Security` `AI AutoMod` `Welcome` `Protections` `Enterprise`\n"
            "`Utilities` `Leveling` `Economy` `Logging` `Music`\n"
            "`Voice` `Events` `Recovery` `Automations` `Counters`"
        )
        embed.add_field(name="📦 Loaded Modules", value=modules_list, inline=False)
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        view = HelpView()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))
