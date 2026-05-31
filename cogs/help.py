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
    def __init__(self, category, main_embed):
        self.category = category
        self.main_embed = main_embed
        
        # Load tools and add the "Back" button at the bottom
        options = [discord.SelectOption(label=tool) for tool in COMMANDS_DB[category].keys()]
        options.append(discord.SelectOption(label="Back", description="Return to main menu", emoji="↩️"))
        
        super().__init__(placeholder="> Select a module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # If they hit Back, show the main embed again
        if self.values[0] == "Back":
            await interaction.response.edit_message(embed=self.main_embed, view=HelpView(self.main_embed))
            return

        tool = self.values[0]
        cmds = COMMANDS_DB[self.category][tool]
        
        embed = discord.Embed(
            title=f"🛠️ {tool} Commands",
            description=f"**Commands:**\n{cmds}",
            color=0x2b2d31
        )
        embed.set_footer(text="Powered by BADNAM Development™ | Developed and designed by subhransudey")
        await interaction.response.edit_message(embed=embed)

class CategorySelect(discord.ui.Select):
    def __init__(self, main_embed):
        self.main_embed = main_embed
        options = [discord.SelectOption(label=cat, emoji=cat.split(" ")[0]) for cat in COMMANDS_DB.keys()]
        super().__init__(placeholder="> Choose a Specific Module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        
        view = discord.ui.View(timeout=180)
        view.add_item(ToolSelect(category, self.main_embed))
        
        # Lists out the tools nicely under the text instead of dots
        tools_list = "\n".join([f"> 🔹 **{tool}**" for tool in COMMANDS_DB[category].keys()])
        
        embed = discord.Embed(
            title=f"{category}",
            description=f"You selected **{category}**.\n\n👇 Pick a specific module below to view commands:\n\n{tools_list}",
            color=0x2b2d31
        )
        embed.set_footer(text="Powered by BADNAM Development™ | Developed and designed by subhransudey")
        await interaction.response.edit_message(embed=embed, view=view)

class HelpView(discord.ui.View):
    def __init__(self, main_embed):
        super().__init__(timeout=180)
        self.add_item(CategorySelect(main_embed))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        total_cmds = sum(len(cmds.split(',')) for cats in COMMANDS_DB.values() for cmds in cats.values())

        embed = discord.Embed(
            title="Hey, I'm BADNAM™",
            description=(
                "A powerful multipurpose bot with the fastest Antinuke.\n"
                "**My Prefix is:** `?`\n"
                f"**Total Commands:** `{total_cmds}+`\n\n"
                "**Choose a Specific Module of your Desire:**\n"
                "> 🛡️ **Security**\n"
                "> ⚙️ **Management**\n"
                "> 💬 **Messaging**\n"
                "> ✨ **Games**\n"
                "> 🎵 **Music**\n\n"
                "**[Invite Me](https://discord.com/oauth2/authorize?client_id=1509404143712993441&permissions=8&integration_type=0&scope=bot+applications.commands) | [Support Server](https://discord.gg/hxJqvcEeBC) | [Website](https://badnam.com)**"
            ),
            color=0x2b2d31
        )
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            
        embed.set_footer(text="Powered by BADNAM Development™ | Developed and designed by subhransudey")
            
        # We pass the embed into the view so the "Back" button can use it later
        await ctx.send(embed=embed, view=HelpView(embed))

async def setup(bot):
    await bot.add_cog(Help(bot))
