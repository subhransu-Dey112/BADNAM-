import discord
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # We create a dropdown for each of your 5 categories
        self.add_item(discord.ui.Select(placeholder="> Security Commands", options=[
            discord.SelectOption(label="Antinuke", description="Protection commands"),
            discord.SelectOption(label="Automod", description="Chat filters"),
            discord.SelectOption(label="Quarantine", description="Isolation tools"),
            discord.SelectOption(label="Adv. Security", description="Deep threat analysis"),
            discord.SelectOption(label="Enterprise Intel", description="Pro-tier defense"),
            discord.SelectOption(label="AI AutoMod", description="Smart moderation")
        ]))
        
        self.add_item(discord.ui.Select(placeholder="> Management Commands", options=[
            discord.SelectOption(label="Tickets", description="Support systems"),
            discord.SelectOption(label="Custom Roles", description="Role management"),
            discord.SelectOption(label="Verification", description="Gatekeeping"),
            discord.SelectOption(label="Moderation", description="Staff toolkit"),
            discord.SelectOption(label="Logging", description="Audit logs")
        ]))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(color=0x2b2d31)
        embed.description = (
            "**My Prefix:** `b!`\n\n"
            "**⚙️ SECURITY**\n🛡️ Antinuke · Automod · Quarantine · Adv. Security · Enterprise Intel · AI AutoMod\n\n"
            "**⚙️ MANAGEMENT**\n🎫 Tickets · Custom Role · Levels · VC Levels · Msg Count · VC Count · Invite Count · AutoRole · Join to Create · Logging · Verification · Moderation · Giveaway · General\n\n"
            "**💬 MESSAGING**\n📌 Sticky · Welcome · Leave · Boost · Auto Respond\n\n"
            "**✨ GAMES**\n🖼️ Pfp Event · Slots · Auto React · Economy · Utils\n\n"
            "**🎵 MUSIC**\n🔊 Music · Voice"
        )
        embed.set_footer(text="SUPPORT | INVITE | WEBSITE | DASHBOARD")
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
