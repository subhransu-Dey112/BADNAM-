import discord
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        # Adding Dropdowns for all 5 categories (Discord allows max 5 per message!)
        self.add_item(discord.ui.Select(placeholder="> Security Commands", options=[
            discord.SelectOption(label="Antinuke", description="Protection commands"),
            discord.SelectOption(label="Automod", description="Chat filters"),
            discord.SelectOption(label="Quarantine", description="Isolation tools"),
            discord.SelectOption(label="Adv. Security", description="Deep threat analysis"),
            discord.SelectOption(label="Enterprise Intel", description="Pro-tier defense"),
            discord.SelectOption(label="AI AutoMod", description="Smart moderation")
        ], custom_id="sec"))
        
        self.add_item(discord.ui.Select(placeholder="> Management Commands", options=[
            discord.SelectOption(label="Tickets", description="Support systems"),
            discord.SelectOption(label="Custom Roles", description="Role management"),
            discord.SelectOption(label="Verification", description="Gatekeeping"),
            discord.SelectOption(label="Moderation", description="Staff toolkit"),
            discord.SelectOption(label="Logging", description="Audit logs")
        ], custom_id="mgt"))

        self.add_item(discord.ui.Select(placeholder="> Messaging Commands", options=[
            discord.SelectOption(label="Sticky", description="Sticky messages"),
            discord.SelectOption(label="Welcome", description="Join messages"),
            discord.SelectOption(label="Leave", description="Leave messages"),
            discord.SelectOption(label="Boost", description="Boost tracker"),
            discord.SelectOption(label="Auto Respond", description="Auto triggers")
        ], custom_id="msg"))

        self.add_item(discord.ui.Select(placeholder="> Games Commands", options=[
            discord.SelectOption(label="Pfp Event", description="Profile picture events"),
            discord.SelectOption(label="Slots", description="Casino slots"),
            discord.SelectOption(label="Auto React", description="Reaction triggers"),
            discord.SelectOption(label="Economy", description="Currency system"),
            discord.SelectOption(label="Utils", description="Fun utilities")
        ], custom_id="game"))

        self.add_item(discord.ui.Select(placeholder="> Music Commands", options=[
            discord.SelectOption(label="Music", description="Audio playback"),
            discord.SelectOption(label="Voice", description="Voice channel tools")
        ], custom_id="mus"))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(color=0x2b2d31)
        
        # Making the list purely vertical with emojis, exactly like the image
        embed.description = (
            "**My Prefix:** `b!`\n\n"
            "**⚙️ SECURITY ⚙️**\n"
            "🛡️ Antinuke\n"
            "🛡️ Automod\n"
            "🛡️ Quarantine\n"
            "🛡️ Adv. Security\n"
            "🛡️ Enterprise Intel\n"
            "🛡️ AI AutoMod\n\n"
            "**⚙️ MANAGEMENT ⚙️**\n"
            "🎫 Tickets\n"
            "🎴 Custom Role\n"
            "📊 Levels\n"
            "🎙️ VC Levels\n"
            "💬 Msg Count\n"
            "🔊 VC Count\n"
            "🔗 Invite Count\n"
            "🐾 AutoRole\n"
            "🎧 Join to Create\n"
            "📂 Logging\n"
            "🚪 Verification\n"
            "🔨 Moderation\n"
            "🎁 Giveaway\n"
            "🌐 General\n\n"
            "**💬 MESSAGING 💬**\n"
            "📌 Sticky\n"
            "👋 Welcome\n"
            "🚪 Leave\n"
            "🚀 Boost\n"
            "🤖 Auto Respond\n\n"
            "**✨ GAMES ✨**\n"
            "🖼️ Pfp Event\n"
            "🎰 Slots\n"
            "⚡ Auto React\n"
            "💵 Economy\n"
            "⚙️ Utils\n\n"
            "**🎵 MUSIC 🎵**\n"
            "🎶 Music\n"
            "🎤 Voice\n\n"
            "**[SUPPORT](https://discord.gg/yourlink) | [INVITE](https://discord.com/oauth2) | [WEBSITE](https://badnam.com) | [DASHBOARD](https://badnam.com/dash)**"
        )
        
        # Adding the thumbnail to the top right
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
