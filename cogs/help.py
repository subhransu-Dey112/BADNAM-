import discord
from discord.ext import commands

# The Master Command Database
COMMANDS_DB = {
    "🛡️ FLOOR 1: SECURITY": {
        "Anti-Nuke": "b!setup, b!antinuke enable/disable, b!antinuke dynamic, b!setlimit, b!quarantine, b!unquarantine, b!panic, b!unpanic, b!backup create/restore, b!trusted add, b!extraowner set, b!sanitize bots/links",
        "AutoMod": "b!automod enable/disable/punishment, b!automod log set/reset/show, b!blackwords add/remove/list, b!antispam enable/limit/duplicate, b!antilink enable/whitelist, b!antiinvite enable/allow-internal, b!automod regex/zalgo/mass-emoji/line-split, b!antimention, b!anticaps, b!antifile",
        "Advanced Security": "b!whois, b!systempanic, b!sanitize all, b!anpanic, b!antinukelog set/reset, b!quarantinerole create",
        "Protections": "b!antidelete channels/roles, b!antibot enable/action, b!antiwebhook, b!trustscore, b!webhook-intercept",
        "Enterprise Intelligence": "b!proxyblocker, b!threatmesh, b!autoquarantine, b!overrideowner, b!bypasscheck, b!strictmode, b!rolemonitor, b!vanityprotect, b!dmreasons",
        "AI AutoMod": "b!ai-mod toxicity, b!ai-mod scam-detection, b!ai-mod image, b!automodlog set, b!automodwhitelist add"
    },
    "🔨 FLOOR 2: ADMINISTRATION": {
        "Moderation": "b!ban, b!softban, b!hackban, b!unban, b!kick, b!timeout, b!untimeout, b!mute, b!unmute, b!tempmute, b!tempban, b!warn, b!warnings, b!delwarn, b!clearwarns, b!reason, b!purge (user/match/embeds/attachments/bots), b!slowmode, b!lock/unlock, b!note add/view/delete",
        "Tickets & Support": "b!ticket enable/disable/add/remove/close/reopen/delete/rename/transcript/list, b!panel create/list/delete/button/message, b!autothread enable/disable/channel add/remove, b!modmail setup/reply/block",
        "Verification": "b!verification enable/disable/setup_role/setup_channel/type/set_verified/reset, b!captcha, b!verify, b!joingate (age/avatar/vpn/action), b!antiraid (sensitivity/join-limit/action), b!username-filter add/list",
        "Recovery": "b!recoverysetup, b!verifychannel, b!verifyrole, b!oauthlink, b!recoverylogs, b!recoverymsg, b!pull, b!pullall, b!stoppull, b!tokenrefresh, b!authusers, b!authcheck, b!authremove, b!authblacklist, b!authclean, b!authexport, b!recoverywl, b!recoverpremium"
    },
    "📈 FLOOR 3: GROWTH": {
        "Utilities": "b!embed create, b!rr setup, b!tag add/list, b!role add/all, b!channel clone, b!poll, b!afk",
        "Leveling": "b!rank, b!leaderboard, b!levelconfig xprate/reward, b!vclevel enable, b!xp add",
        "Economy": "b!balance, b!work, b!daily, b!crime, b!deposit, b!withdraw, b!shop, b!buy, b!slots, b!roulette, b!blackjack, b!meme, b!pokemon, b!addmoney",
        "Music & Voice": "b!play, b!stop, b!pause, b!skip, b!queue, b!loop, b!volume, b!filter, b!autovoice setup, b!vc lock/unlock/kick, b!vcrole set",
        "Events & Counters": "b!giveaway start/reroll, b!starboard, b!suggest, b!suggestion approve, b!leave enable, b!boostmessage enable, b!invites, b!messagescount show, b!voicecount show, b!avatar, b!banner",
        "Automation & Misc": "b!autorespond add, b!autoreact add, b!sticky add, b!autologs enable/setup/set, b!cases, b!diagnose, b!stats, b!help"
    }
}

class ToolSelect(discord.ui.Select):
    def __init__(self, category, main_embed):
        self.category = category
        self.main_embed = main_embed
        options = [discord.SelectOption(label=tool) for tool in COMMANDS_DB[category].keys()]
        options.append(discord.SelectOption(label="Back", description="Return to main menu", emoji="↩️"))
        super().__init__(placeholder="> Select a specific module...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Back":
            await interaction.response.edit_message(embed=self.main_embed, view=HelpView(self.main_embed))
            return
        tool = self.values[0]
        cmds = COMMANDS_DB[self.category][tool]
        embed = discord.Embed(title=f"🛠️ {tool} Commands", description=f"**Usage:**\n{cmds}", color=0x2b2d31)
        embed.set_footer(text="Powered by BADNAM Development™ | Developed by subhransudey")
        await interaction.response.edit_message(embed=embed)

class CategorySelect(discord.ui.Select):
    def __init__(self, main_embed):
        self.main_embed = main_embed
        options = [discord.SelectOption(label=cat, emoji=cat.split(" ")[0]) for cat in COMMANDS_DB.keys()]
        super().__init__(placeholder="> Choose a Floor to begin...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        view = discord.ui.View(timeout=180).add_item(ToolSelect(category, self.main_embed))
        tools = "\n".join([f"> 🔹 **{t}**" for t in COMMANDS_DB[category].keys()])
        embed = discord.Embed(title=f"{category}", description=f"You selected **{category}**.\n\n👇 Pick a module below to view commands:\n\n{tools}", color=0x2b2d31)
        embed.set_footer(text="Powered by BADNAM Development™ | Developed by subhransudey")
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
        embed = discord.Embed(
            title="Hey, I'm BADNAM™",
            description=(
                "A powerful multipurpose bot with the fastest Antinuke.\n"
                "**My Prefix is:** `b!`\n"
                "**Total Commands:** `221+`\n\n"
                "**Choose a Floor to view modules:**\n"
                "> 🛡️ **FLOOR 1: SECURITY & DEFENSE**\n"
                "> 🔨 **FLOOR 2: ADMINISTRATION & SUPPORT**\n"
                "> 📈 **FLOOR 3: GROWTH & INTERACTION**\n\n"
                "**[Invite Me](https://discord.com/oauth2/authorize?client_id=1509404143712993441&permissions=8&integration_type=0&scope=bot+applications.commands) | [Support Server](https://discord.gg/hxJqvcEeBC) | [Website](https://badnam.com)**"
            ),
            color=0x2b2d31
        )
        if self.bot.user.avatar: embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Powered by BADNAM Development™ | Developed by subhransudey")
        await ctx.send(embed=embed, view=HelpView(embed))

async def setup(bot):
    await bot.add_cog(Help(bot))
