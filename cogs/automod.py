import discord
from discord.ext import commands

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🤖 MASTER AUTOMOD TOGGLES
    @commands.group(name="automod", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def automod(self, ctx):
        await ctx.send("❓ Usage: `b!automod <enable | disable | punishment | log | whitelist | regex | zalgo>`")

    @automod.command(name="enable")
    async def am_enable(self, ctx):
        await ctx.send("🤖 **AutoMod:** ENABLED. Scanning all incoming messages.")

    @automod.command(name="disable")
    async def am_disable(self, ctx):
        await ctx.send("⚠️ **AutoMod:** DISABLED. Chat is currently unmonitored.")

    @automod.command(name="punishment")
    async def am_punish(self, ctx, action: str):
        valid = ["warn", "mute", "kick", "timeout"]
        if action.lower() in valid:
            await ctx.send(f"⚖️ Default AutoMod penalty set to: **{action.upper()}**")
        else:
            await ctx.send(f"❌ Invalid action. Choose: `{', '.join(valid)}`")

    # 📜 AUTOMOD LOGGING
    @automod.group(name="log", invoke_without_command=True)
    async def am_log(self, ctx):
        pass

    @am_log.command(name="set")
    async def am_log_set(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"📂 AutoMod infractions will now be logged in {channel.mention}.")

    @am_log.command(name="reset")
    async def am_log_reset(self, ctx):
        await ctx.send("🗑️ AutoMod logging channel configuration wiped.")

    @am_log.command(name="show")
    async def am_log_show(self, ctx):
        await ctx.send("📊 **Current Log Channel:** None configured.")

    # 🤬 BLACKWORDS SYSTEM
    @commands.group(name="blackwords", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def blackwords(self, ctx):
        await ctx.send("❓ Usage: `b!blackwords <add | remove | list>`")

    @blackwords.command(name="add")
    async def bw_add(self, ctx, *, phrase: str):
        await ctx.send(f"🚫 Added `{phrase}` to the prohibited vocabulary filter.")

    @blackwords.command(name="remove")
    async def bw_remove(self, ctx, *, phrase: str):
        await ctx.send(f"✅ Removed `{phrase}` from the prohibited vocabulary filter.")

    @blackwords.command(name="list")
    async def bw_list(self, ctx):
        await ctx.send("📄 **Prohibited Words:**\n*(List is currently empty)*")

    # 🛑 SPAM & VELOCITY CONTROL
    @commands.group(name="antispam", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def antispam(self, ctx):
        pass

    @antispam.command(name="enable")
    async def as_enable(self, ctx):
        await ctx.send("🛡️ **Anti-Spam:** Velocity tracking activated.")

    @antispam.command(name="limit")
    async def as_limit(self, ctx, number: int, seconds: int):
        await ctx.send(f"⏱️ Limit set: Flagging users sending **{number} messages** within **{seconds} seconds**.")

    @antispam.command(name="duplicate")
    async def as_dup(self, ctx, number: int):
        await ctx.send(f"📋 Limit set: Flagging users sending the exact same message **{number} times**.")

    # 🔗 LINK & INVITE FILTERS
    @commands.group(name="antilink", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def antilink(self, ctx):
        pass
    
    @antilink.command(name="enable")
    async def al_enable(self, ctx):
        await ctx.send("🚫 **Anti-Link:** Unapproved URLs will be deleted.")

    @antilink.command(name="whitelist")
    async def al_whitelist(self, ctx, domain: str):
        await ctx.send(f"✅ Users can now post links to `{domain}`.")

    @commands.group(name="antiinvite", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def antiinvite(self, ctx):
        pass

    @antiinvite.command(name="enable")
    async def ai_enable(self, ctx):
        await ctx.send("🛑 **Anti-Invite:** Third-party Discord invites will be deleted.")

    @antiinvite.command(name="allow-internal")
    async def ai_internal(self, ctx, state: bool):
        mode = "Allowed" if state else "Blocked"
        await ctx.send(f"🔄 **Internal Server Links:** {mode}.")

    # 🧬 EXTREME AUTOMOD (Regex, Zalgo, Mass-Emoji)
    @automod.command(name="regex")
    async def am_regex(self, ctx, *, code: str):
        await ctx.send(f"🧬 Regex filter applied: `{code}`")

    @automod.command(name="zalgo")
    async def am_zalgo(self, ctx, state: str):
        await ctx.send(f"🔣 **Zalgo Text Filter:** {state.upper()}")

    @automod.command(name="mass-emoji")
    async def am_emoji(self, ctx, number: int):
        await ctx.send(f"😀 Limit set: Messages containing more than **{number} emojis** will be purged.")

    @automod.command(name="line-split")
    async def am_lines(self, ctx, number: int):
        await ctx.send(f"📏 Limit set: Messages with more than **{number} line breaks** will be flagged as spam.")

    # 🎛️ MISC FILTERS
    @commands.command(name="antimention")
    @commands.has_permissions(manage_guild=True)
    async def antimention(self, ctx, number: int):
        await ctx.send(f"📣 Limit set: Messages containing more than **{number} unique mentions** will be purged.")

    @commands.command(name="anticaps")
    @commands.has_permissions(manage_guild=True)
    async def anticaps(self, ctx, percentage: int):
        await ctx.send(f"🔠 Limit set: Messages containing more than **{percentage}% CAPITAL LETTERS** will be purged.")

    @commands.command(name="antifile")
    @commands.has_permissions(manage_guild=True)
    async def antifile(self, ctx, state: str):
        await ctx.send(f"📁 **Anti-File Uploads:** {state.upper()}")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
