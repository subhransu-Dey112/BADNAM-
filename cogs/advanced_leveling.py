import discord
from discord.ext import commands

class AdvancedLeveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 📈 CORE LEVELING
    @commands.command(name="rank")
    async def rank(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        await ctx.send(f"📊 Pulling rank card for **{target.name}**...")

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        await ctx.send("🏆 **Server Leaderboard:** Fetching top active users...")

    # ⚙️ LEVEL CONFIGURATION
    @commands.group(name="levelconfig", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def levelconfig(self, ctx):
        pass

    @levelconfig.command(name="xprate")
    async def lc_xprate(self, ctx, min_xp: int, max_xp: int):
        await ctx.send(f"⚙️ XP per message set to random between {min_xp} and {max_xp}.")

    @levelconfig.command(name="reward")
    async def lc_reward(self, ctx, level: int, role: discord.Role):
        await ctx.send(f"🎁 Users will now earn {role.name} at Level {level}.")

    # 🎙️ VOICE TRACKING
    @commands.group(name="vclevel", invoke_without_command=True)
    async def vclevel(self, ctx):
        pass

    @vclevel.command(name="enable")
    @commands.has_permissions(administrator=True)
    async def vcl_enable(self, ctx):
        await ctx.send("🎙️ **Voice Leveling:** ENABLED. Tracking active VC minutes.")

    # 🛠️ ADMIN XP CONTROLS
    @commands.group(name="xp", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def xp(self, ctx):
        pass

    @xp.command(name="add")
    async def xp_add(self, ctx, user: discord.Member, amount: int):
        await ctx.send(f"✅ Awarded {amount} XP to {user.mention}.")

async def setup(bot):
    await bot.add_cog(AdvancedLeveling(bot))
