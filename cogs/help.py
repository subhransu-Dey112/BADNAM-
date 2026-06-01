import discord
from discord.ext import commands

# The 2-Tier Command Database
COMMANDS_DB = {
    "sec": {
        "title": "🛡️ SECURITY",
        "emoji": "🛡️",
        "modules": {
            "Anti-Nuke": "b!setup, b!antinuke enable/disable, b!antinuke dynamic, b!setlimit, b!quarantine, b!unquarantine",
            "AutoMod": "b!automod enable/disable, b!blackwords, b!antispam, b!antilink, b!antiinvite",
            "Advanced": "b!whois, b!systempanic, b!anpanic, b!antinukelog, b!quarantinerole",
            "Protections": "b!antidelete, b!antibot, b!antiwebhook, b!trustscore, b!webhook-intercept",
            "AI AutoMod": "b!ai-mod toxicity/scam/image, b!automodlog, b!automodwhitelist"
        }
    },
    "man": {
        "title": "⚙️ MANAGEMENT",
        "emoji": "⚙️",
        "modules": {
            "Tickets": "b!ticket enable/close/transcript, b!panel create/button, b!autothread, b!modmail",
            "Custom Roles": "b!autorole, b!vcrole, b!joinrole",
            "Levels": "b!rank, b!levelconfig, b!xp",
            "Logging": "b!autologs, b!cases, b!diagnose",
            "Verification": "b!verification setup, b!captcha, b!verify, b!joingate, b!antiraid, b!username-filter",
            "Moderation": "b!ban, b!softban, b!hackban, b!unban, b!kick, b!timeout, b!mute, b!warn, b!purge",
            "Giveaway": "b!giveaway start/reroll/end, b!greroll",
            "General": "b!ping, b!stats, b!uptime, b!invite"
        }
    },
    "msg": {
        "title": "💬 MESSAGING",
        "emoji": "💬",
        "modules": {
            "Essentials": "b!sticky, b!welcome, b!leave, b!boostmessage",
            "Interaction": "b!autorespond, b!autoreact, b!suggest, b!starboard"
        }
    },
    "gam": {
        "title": "✨ GAMES",
        "emoji": "✨",
        "modules": {
            "Economy": "b!balance, b!work, b!daily, b!crime, b!shop, b!slots, b!roulette, b!blackjack",
            "Utils": "b!embed, b!rr setup, b!tag, b!role, b!channel, b!poll, b!afk"
        }
    },
    "mus": {
        "title": "🎵 MUSIC",
        "emoji": "🎵",
        "modules": {
            "Playback": "b!play, b!stop, b!pause, b!skip, b!queue, b!loop, b!volume",
            "Voice": "b!autovoice, b!vc lock/unlock/kick"
        }
    }
}

# --- VIEW 2: THE SUB-MODULE DROPDOWN ---
class ModuleDropdown(discord.ui.Select):
    def __init__(self, category_key, main_embed):
        self.category_key = category_key
        self.main_embed = main_embed
        self.data = COMMANDS_DB[category_key]
        
        options = []
        for mod_name in self.data["modules"].keys():
            options.append(discord.SelectOption(label=mod_name, emoji="🔹"))
        
        options.append(discord.SelectOption(label="Go Back", value="back", emoji="↩️"))
        super().__init__(placeholder="> Select a module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # If they click Go Back, return to the Main Menu
        if self.values[0] == "back":
            await interaction.response.edit_message(embed=self.main_embed, view=MainView(self.main_embed))
            return

        # Show the commands for the selected module
        mod_name = self.values[0]
        commands_str = self.data["modules"][mod_name]
        
        embed = discord.Embed(
            title=f"{self.data['emoji']} {mod_name.upper()}",
            description=f"Here are the commands for **{mod_name}**:\n\n```{commands_str}```",
            color=0x2b2d31
        )
        
        if interaction.client.user.avatar:
            embed.set_thumbnail(url=interaction.client.user.avatar.url)
        embed.set_footer(
            text="Powered by BADNAM Development™ | Developed and designed by subhransudey", 
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )
        
        # Keep them in the ModuleView so they can check other modules in the same category
        await interaction.response.edit_message(embed=embed, view=ModuleView(self.category_key, self.main_embed))

class ModuleView(discord.ui.View):
    def __init__(self, category_key, main_embed):
        super().__init__(timeout=180)
        self.add_item(ModuleDropdown(category_key, main_embed))

# --- VIEW 1: THE MAIN CATEGORY DROPDOWN ---
class MainDropdown(discord.ui.Select):
    def __init__(self, main_embed):
        self.main_embed = main_embed
        options = [
            discord.SelectOption(label="Security", value="sec", emoji="🛡️"),
            discord.SelectOption(label="Management", value="man", emoji="⚙️"),
            discord.SelectOption(label="Messaging", value="msg", emoji="💬"),
            discord.SelectOption(label="Games", value="gam", emoji="✨"),
            discord.SelectOption(label="Music", value="mus", emoji="🎵")
        ]
        super().__init__(placeholder="> Choose a Specific Module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category_key = self.values[0]
        data = COMMANDS_DB[category_key]
        
        # Build the beautiful blockquote list exactly like your screenshot
        desc = f"You selected {data['emoji']} **{data['title'].replace(data['emoji'] + ' ', '')}**.\n\n👇 Pick a specific module below to view commands:\n\n>>> "
        
        for mod_name in data["modules"].keys():
            desc += f"🔹 **{mod_name}**\n"
            
        embed = discord.Embed(
            title=data["title"],
            description=desc,
            color=0x2b2d31
        )
        
        if interaction.client.user.avatar:
            embed.set_thumbnail(url=interaction.client.user.avatar.url)
        embed.set_footer(
            text="Powered by BADNAM Development™ | Developed and designed by subhransudey", 
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )
        
        # Switch the dropdown to the Module Selection view
        await interaction.response.edit_message(embed=embed, view=ModuleView(category_key, self.main_embed))

class MainView(discord.ui.View):
    def __init__(self, main_embed):
        super().__init__(timeout=180)
        self.add_item(MainDropdown(main_embed))

# --- THE HELP COMMAND ---
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def custom_help(self, ctx):
        prefix = ctx.prefix

        embed = discord.Embed(
            title="Hey, I'm BADNAM™",
            description=(
                f"A powerful multipurpose bot with the fastest Antinuke.\n"
                f"**My Prefix is:** `{prefix}`\n"
                f"**Total Commands:** `221+`\n\n"
                f"**Choose a Specific Module of your Desire:**\n"
                f"🛡️ Security\n"
                f"⚙️ Management\n"
                f"💬 Messaging\n"
                f"✨ Games\n"
                f"🎵 Music\n\n"
                f"[Invite Me](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot) | "
                f"[Support Server](https://discord.gg/hxJqvcEeBC) | "
                f"[Website](https://badnam-1.onrender.com)"
            ),
            color=0x2b2d31
        )

        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed.set_footer(
            text="Powered by BADNAM Development™ | Developed and designed by subhransudey",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )

        await ctx.send(embed=embed, view=MainView(embed))

async def setup(bot):
    await bot.add_cog(Help(bot))
