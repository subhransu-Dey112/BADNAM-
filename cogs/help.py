import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    def __init__(self, placeholder, options):
        super().__init__(placeholder=placeholder, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected {self.values[0]}! (Commands coming soon)", ephemeral=True)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        
        self.add_item(HelpDropdown("> Security Commands", [
            discord.SelectOption(label="Antinuke"), discord.SelectOption(label="Automod"), 
            discord.SelectOption(label="Quarantine"), discord.SelectOption(label="Adv. Security"), 
            discord.SelectOption(label="Enterprise Intel"), discord.SelectOption(label="AI AutoMod")
        ]))
        
        self.add_item(HelpDropdown("> Management Commands", [
            discord.SelectOption(label="Tickets"), discord.SelectOption(label="Custom Roles"), 
            discord.SelectOption(label="Levels"), discord.SelectOption(label="VC Levels"),
            discord.SelectOption(label="Msg Count"), discord.SelectOption(label="VC Count"),
            discord.SelectOption(label="Invite Count"), discord.SelectOption(label="AutoRole"),
            discord.SelectOption(label="Join to Create"), discord.SelectOption(label="Logging"),
            discord.SelectOption(label="Verification"), discord.SelectOption(label="Moderation"), 
            discord.SelectOption(label="Giveaway"), discord.SelectOption(label="General")
        ]))

        self.add_item(HelpDropdown("> Messaging Commands", [
            discord.SelectOption(label="Sticky"), discord.SelectOption(label="Welcome"), 
            discord.SelectOption(label="Leave"), discord.SelectOption(label="Boost"), 
            discord.SelectOption(label="Auto Respond")
        ]))

        self.add_item(HelpDropdown("> Games Commands", [
            discord.SelectOption(label="Pfp Event"), discord.SelectOption(label="Slots"), 
            discord.SelectOption(label="Auto React"), discord.SelectOption(label="Economy"), 
            discord.SelectOption(label="Utils")
        ]))

        self.add_item(HelpDropdown("> Music Commands", [
            discord.SelectOption(label="Music"), discord.SelectOption(label="Voice")
        ]))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        embed = discord.Embed(color=0xffcc00) # Trident Yellow
        
        embed.description = (
            "**My Prefix:** `b!`\n\n"
            "**⚙️ SECURITY ⚙️**\n"
            "🛡️ Antinuke\n🛡️ Automod\n🛡️ Quarantine\n🛡️ Adv. Security\n🛡️ Enterprise Intel\n🛡️ AI AutoMod\n\n"
            "**⚙️ MANAGEMENT ⚙️**\n"
            "🎫 Tickets\n🎴 Custom Role\n📊 Levels\n🎙️ VC Levels\n💬 Msg Count\n🔊 VC Count\n🔗 Invite Count\n"
            "🐾 AutoRole\n🎧 Join to Create\n📂 Logging\n🚪 Verification\n🔨 Moderation\n🎁 Giveaway\n🌐 General\n\n"
            "**💬 MESSAGING 💬**\n"
            "📌 Sticky\n👋 Welcome\n🚪 Leave\n🚀 Boost\n🤖 Auto Respond\n\n"
            "**✨ GAMES ✨**\n"
            "🖼️ Pfp Event\n🎰 Slots\n⚡ Auto React\n💵 Economy\n⚙️ Utils\n\n"
            "**🎵 MUSIC 🎵**\n"
            "🎶 Music\n🎤 Voice\n\n"
            "**[SUPPORT](https://discord.gg/yourlink) | [INVITE](https://discord.com/oauth2) | [WEBSITE](https://badnam.com) | [DASHBOARD](https://badnam.com/dash)**"
        )
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
