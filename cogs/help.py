import discord
from discord.ext import commands

# The 2-Tier Command Database - Fully Assembled
COMMANDS_DB = {
    "aut": {
        "title": "🤖 AUTOMATION",
        "emoji": "🤖",
        "modules": {
            "AutoRole Humans": (
                "> 🧑 `b!autorole humans` • Shows current human roles\n"
                "> ➕ `b!autorole humans add` • Adds an auto-role for humans\n"
                "> ➖ `b!autorole humans remove` • Removes a human auto-role"
            ),
            "AutoRole Bots": (
                "> 🤖 `b!autorole bots` • Shows current bot roles\n"
                "> ➕ `b!autorole bots add` • Adds an auto-role for bots\n"
                "> ➖ `b!autorole bots remove` • Removes a bot auto-role"
            ),
            "AutoRole Admin": (
                "> ⚙️ `b!autorole config` • Lists all configurations\n"
                "> 🧑‍ `b!autorole reset humans` • Clears human lists\n"
                "> 🤖‍ `b!autorole reset bots` • Clears bot lists\n"
                "> 🧹 `b!autorole reset all` • Fully wipes the system"
            )
        }
    },
    "sec": {
        "title": "🛡️ SECURITY",
        "emoji": "🛡️",
        "modules": {
            "Anti-Nuke": (
                "> 🛡️ `b!antinuke enable` • Turns on 24/7 protection\n"
                "> 🛑 `b!antinuke disable` • Shuts down protection"
            ),
            "Anti-Nuke Logs": (
                "> 📡 `b!antinukelog set` • Sets the alert channel\n"
                "> 🗑️ `b!antinukelog reset` • Removes alert channel\n"
                "> 🔭 `b!antinukelog show` • Shows log channel\n"
                "> 💬 `b!antinukelog msg` • Sets custom alert message"
            ),
            "Anti-Nuke Whitelist": (
                "> ✅ `b!whitelist [@user]` • Adds a bypass user\n"
                "> ❌ `b!whitelist remove` • Removes a user\n"
                "> 📋 `b!whitelist show` • Lists all whitelisted\n"
                "> 🧹 `b!whitelist resetall` • Clears the list"
            ),
            "Extra Owner": (
                "> 👑 `b!extraowner set` • Grants owner bypass\n"
                "> ⛔ `b!extraowner remove` • Removes bypass\n"
                "> 📜 `b!extraowner list` • Lists all extra owners\n"
                "> 🔄 `b!extraowner reset` • Wipes the list"
            ),
            "AutoMod Core": (
                "> ⚙️ `b!automod enable` • Turns on AutoMod\n"
                "> 🛑 `b!automod disable` • Shuts down AutoMod\n"
                "> 🎛️ `b!automod config` • Shows settings & toggles\n"
                "> 🔄 `b!automod reset` • Wipes settings to default\n"
                "> 🛠️ `b!automod manage` • Toggles specific filters"
            ),
            "AutoMod Punish & Log": (
                "> ⚖️ `b!automod punishment set` • Sets timeout/kick/ban\n"
                "> 👁️ `b!automod punishment show` • Checks punishment\n"
                "> 🔄 `b!automod punishment reset` • Resets to timeout\n"
                "> 📡 `b!automod log set` • Sets action report channel\n"
                "> 🗑️ `b!automod log reset` • Disables logging\n"
                "> 🔭 `b!automod log show` • Shows log channel"
            ),
            "AutoMod Ignore": (
                "> ✅ `b!automod ignore add` • Ignores role/channel\n"
                "> ❌ `b!automod ignore remove` • Removes bypass\n"
                "> 🔓 `b!automod unignore` • Specific unignore\n"
                "> 📋 `b!automod ignore show` • Lists all bypasses\n"
                "> 🧹 `b!automod ignore reset` • Clears ignore list"
            ),
            "AntiBot": (
                "> 🤖 `b!antibot add` • Turns on AntiBot\n"
                "> 🛑 `b!antibot remove` • Turns off AntiBot\n"
                "> ✅ `b!antibot wl` • Whitelists a Bot ID\n"
                "> 🎛️ `b!antibot config` • Shows AntiBot status\n"
                "> 🔄 `b!antibot reset` • Turns off & wipes list"
            )
        }
    },
    "man": {
        "title": "⚙️ MANAGEMENT",
        "emoji": "⚙️",
        "modules": {
            "Moderation": (
                "> 👢 `b!kick [@user]` • Kicks a member\n"
                "> 🔨 `b!ban [@user]` • Permanently bans a member\n"
                "> 🕊️ `b!unban [ID]` • Unbans a user via ID\n"
                "> ⏱️ `b!mute [@user] [m]` • Times out a member\n"
                "> 🔊 `b!unmute [@user]` • Removes a timeout early\n"
                "> ⚠️ `b!warn [@user]` • Adds a warning to a member\n"
                "> 📋 `b!warn list [@user]` • Views a member's warnings\n"
                "> 🗑️ `b!warn clear [@user]` • Clears a member's warnings\n"
                "> 🏷️ `b!nick [@user] [name]` • Changes a nickname\n"
                "> 🎭 `b!role [@user] [@role]` • Toggles a role on a user\n"
                "> 🧹 `b!purge [amount]` • Mass deletes messages\n"
                "> 👤 `b!purge user [@user]` • Deletes user's msgs\n"
                "> 🎯 `b!snipe` • Recalls last deleted message"
            ),
            "Server & Channel": (
                "> 🔒 `b!lock` • Prevents typing in channel\n"
                "> 🔓 `b!unlock` • Allows typing in channel\n"
                "> 👻 `b!hide` • Makes channel invisible\n"
                "> 👁️ `b!unhide` • Makes channel visible\n"
                "> ☢️ `b!nuke` • Clones and wipes the channel\n"
                "> 🛑 `b!lockall` • Locks ALL text channels\n"
                "> 🟢 `b!unlockall` • Unlocks ALL text channels\n"
                "> 🙈 `b!hideall` • Hides ALL text channels\n"
                "> 🐵 `b!unhideall` • Unhides ALL text channels\n"
                "> 👥 `b!roleall [@role]` • Gives role to ALL humans\n"
                "> 🎙️ `b!unmuteall` • Unmutes everyone in VC"
            ),
            "Tickets": "`b!ticket`, `b!panel`, `b!autothread`, `b!modmail`",
            "Verification": "`b!verification`, `b!captcha`, `b!verify`, `b!joingate`, `b!antiraid`"
        }
    },
    "msg": {
        "title": "💬 MESSAGING",
        "emoji": "💬",
        "modules": {
            "Auto Responder": (
                "> 💬 `b!att add [trig] | [rep]` • Adds auto-reply\n"
                "> ✏️ `b!att edit [trig] | [rep]` • Edits a reply\n"
                "> 🗑️ `b!att remove [trig]` • Deletes a trigger\n"
                "> ⏱️ `b!att autodel [trig] [s]` • Auto-deletes bot reply\n"
                "> 📋 `b!att list` • Lists all auto-replies\n"
                "> 🧹 `b!att reset` • Clears all auto-replies"
            ),
            "Auto React": (
                "> ✨ `b!react add [trig] | [emj]` • Adds an auto-react\n"
                "> 🗑️ `b!react remove [trig]` • Removes an auto-react\n"
                "> 📋 `b!react list` • Lists all auto-reacts\n"
                "> 🧹 `b!react reset` • Clears all auto-reacts"
            ),
            "Essentials": "`b!sticky`, `b!welcome`, `b!leave`, `b!boostmessage`"
        }
    },
    "gam": {
        "title": "✨ GAMES",
        "emoji": "✨",
        "modules": {
            "Economy": "`b!balance`, `b!work`, `b!daily`, `b!crime`, `b!shop`, `b!slots`, `b!roulette`",
            "Utils": "`b!embed`, `b!rr setup`, `b!tag`, `b!channel`, `b!poll`, `b!afk`"
        }
    },
    "mus": {
        "title": "🎵 MUSIC",
        "emoji": "🎵",
        "modules": {
            "Playback": "`b!play`, `b!stop`, `b!pause`, `b!skip`, `b!queue`, `b!loop`, `b!volume`",
            "Voice": "`b!autovoice`, `b!vc lock/unlock/kick`"
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
        if self.values[0] == "back":
            await interaction.response.edit_message(embed=self.main_embed, view=MainView(self.main_embed))
            return

        mod_name = self.values[0]
        commands_str = self.data["modules"][mod_name]
        
        embed = discord.Embed(
            title=f"{self.data['emoji']} {mod_name.upper()}",
            description=f"Here are the commands for **{mod_name}**:\n\n{commands_str}",
            color=0x2b2d31
        )
        
        if interaction.client.user.avatar:
            embed.set_thumbnail(url=interaction.client.user.avatar.url)
        embed.set_footer(
            text="Powered by BADNAM Development™ | Developed and designed by subhransudey", 
            icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
        )
        
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
            discord.SelectOption(label="Automation", value="aut", emoji="🤖"),
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
                f"**Total Commands:** `230+`\n\n"
                f"**Choose a Specific Module of your Desire:**\n"
                f"🤖 Automation\n"
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
