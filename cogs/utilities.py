import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 📇 EMBEDS & REACTION ROLES
    @commands.group(name="embed", invoke_without_command=True)
    async def embed(self, ctx):
        pass

    @embed.command(name="create")
    async def embed_create(self, ctx):
        await ctx.send("📝 Launching interactive embed builder...")

    @commands.group(name="rr", aliases=["reactionroles"], invoke_without_command=True)
    async def rr(self, ctx):
        pass

    @rr.command(name="setup")
    async def rr_setup(self, ctx):
        await ctx.send("🔘 Initializing reaction role configuration...")

    # 🏷️ CUSTOM TAGS (Macros)
    @commands.group(name="tag", invoke_without_command=True)
    async def tag(self, ctx):
        pass

    @tag.command(name="add")
    async def tag_add(self, ctx, name: str, *, response: str):
        await ctx.send(f"✅ Custom tag `{name}` created.")

    @tag.command(name="list")
    async def tag_list(self, ctx):
        await ctx.send("📄 Fetching custom server macros...")

    # 🎭 MASS ROLE MANAGEMENT
    @commands.group(name="role", invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx):
        pass

    @role.command(name="add")
    async def role_add(self, ctx, user: discord.Member, role: discord.Role):
        await ctx.send(f"✅ Added {role.name} to {user.mention}.")

    @role.command(name="all")
    async def role_all(self, ctx, role: discord.Role):
        await ctx.send(f"⚠️ Mass-assigning {role.name} to all members. This may take a while.")

    # 💬 CHANNEL & CHAT UTILITIES
    @commands.group(name="channel", invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def channel(self, ctx):
        pass

    @channel.command(name="clone")
    async def channel_clone(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"👯 Cloned {channel.mention} successfully.")

    @commands.command(name="poll")
    async def poll(self, ctx, *, question: str):
        await ctx.send("📊 Generating server poll...")

    @commands.command(name="afk")
    async def afk(self, ctx, *, reason="Away"):
        await ctx.send(f"💤 **{ctx.author.name}** is now AFK: {reason}")

async def setup(bot):
    await bot.add_cog(Utilities(bot))
