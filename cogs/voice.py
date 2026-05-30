import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="autovoice", aliases=["jtc"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def autovoice(self, ctx):
        pass

    @autovoice.command(name="setup")
    async def av_setup(self, ctx):
        await ctx.send("🎙️ Generating Master 'Join-to-Create' voice channel...")

    @commands.group(name="vc", invoke_without_command=True)
    async def vc(self, ctx):
        pass

    @vc.command(name="lock")
    async def vc_lock(self, ctx):
        await ctx.send("🔒 Your temporary voice channel is now locked.")

    @vc.command(name="unlock")
    async def vc_unlock(self, ctx):
        await ctx.send("🔓 Your temporary voice channel is now open.")

    @vc.command(name="kick")
    async def vc_kick(self, ctx, user: discord.Member):
        await ctx.send(f"👢 Kicked {user.mention} from your voice channel.")

    @commands.group(name="vcrole", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def vcrole(self, ctx):
        pass

    @vcrole.command(name="set")
    async def vcr_set(self, ctx, role: discord.Role):
        await ctx.send(f"🔗 Users joining voice will now temporarily get the {role.name} role.")

async def setup(bot):
    await bot.add_cog(Voice(bot))
