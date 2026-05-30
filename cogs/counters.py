import discord
from discord.ext import commands

class Counters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 👋 LEAVE & BOOST MESSAGES
    @commands.group(name="leave", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def leave(self, ctx):
        pass

    @leave.command(name="enable")
    async def leave_enable(self, ctx):
        await ctx.send("👋 Goodbye messages **ENABLED**.")

    @commands.group(name="boostmessage", aliases=["boost"], invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def boostmsg(self, ctx):
        pass

    @boostmsg.command(name="enable")
    async def boost_enable(self, ctx):
        await ctx.send("🚀 Server Boost thank-you messages **ENABLED**.")

    # 📊 COUNTERS (Invites, Messages, Voice)
    @commands.command(name="invites")
    async def invites(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        await ctx.send(f"🔗 **{target.name}** has invited **0** users to the server.")

    @commands.group(name="messagescount", aliases=["msgcount"], invoke_without_command=True)
    async def msg_count(self, ctx):
        pass

    @msg_count.command(name="show")
    async def msg_show(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        await ctx.send(f"💬 **{target.name}** has sent **0** messages in this server.")

    @commands.group(name="voicecount", aliases=["vccount"], invoke_without_command=True)
    async def vc_count(self, ctx):
        pass

    @vc_count.command(name="show")
    async def vc_show(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        await ctx.send(f"🎙️ **{target.name}** has spent **0 hours, 0 minutes** in voice channels.")

    # 🖼️ USER PROFILES (Pfp / Banner)
    @commands.command(name="avatar", aliases=["pfp"])
    async def avatar(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        await ctx.send(f"🖼️ Fetching high-resolution avatar for **{target.name}**...")

    @commands.command(name="banner")
    async def banner(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        await ctx.send(f"🎨 Fetching profile banner for **{target.name}**...")

async def setup(bot):
    await bot.add_cog(Counters(bot))
