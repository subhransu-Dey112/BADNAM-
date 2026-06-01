import discord
from discord.ext import commands
import datetime
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {} # Stores deleted messages for b!snipe

    # --- LISTENER FOR SNIPE ---
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return
        self.snipes[message.channel.id] = {
            "content": message.content,
            "author": message.author,
            "time": discord.utils.utcnow()
        }

    # --- BASIC MODERATION ---
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"✅ **{member.name}** was kicked.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.name}** was banned.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason="No reason"):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"✅ **{user.name}** was unbanned.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int = 10, *, reason="No reason"):
        duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"⏱️ **{member.name}** muted for {minutes}m.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 **{member.name}** was unmuted.")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, name=None):
        await member.edit(nick=name)
        await ctx.send(f"✅ Nickname updated for **{member.name}**.")

    @commands.command()
    async def snipe(self, ctx):
        snipe_data = self.snipes.get(ctx.channel.id)
        if not snipe_data:
            return await ctx.send("❌ Nothing to snipe!")
        embed = discord.Embed(description=snipe_data["content"], color=0x2b2d31)
        embed.set_author(name=snipe_data["author"], icon_url=snipe_data["author"].display_avatar.url)
        embed.set_footer(text=f"Deleted at {snipe_data['time'].strftime('%H:%M:%S')}")
        await ctx.send(embed=embed)

    # --- CHANNEL MANAGEMENT (Lock, Hide, Nuke, Slowmode) ---
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"🔒 {channel.mention} is now locked.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"🔓 {channel.mention} is now unlocked.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await ctx.send(f"👻 {channel.mention} is now hidden.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        await ctx.send(f"👁️ {channel.mention} is now visible.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"⏱️ Slowmode set to {seconds} seconds.")

    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def nuke(self, ctx):
        channel = ctx.channel
        position = channel.position
        new_channel = await channel.clone(reason="Channel Nuked")
        await channel.delete()
        await new_channel.edit(position=position)
        await new_channel.send("💥 Channel has been nuked!")

    # --- ADVANCED PURGE SYSTEM ---
    @commands.group(invoke_without_command=True, aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"✅ Purged {amount} messages.", delete_after=3)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def bots(self, ctx, amount: int = 50):
        def is_bot(m): return m.author.bot
        deleted = await ctx.channel.purge(limit=amount, check=is_bot)
        await ctx.send(f"✅ Purged {len(deleted)} bot messages.", delete_after=3)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx, member: discord.Member, amount: int = 50):
        def is_user(m): return m.author == member
        deleted = await ctx.channel.purge(limit=amount, check=is_user)
        await ctx.send(f"✅ Purged {len(deleted)} messages from {member.name}.", delete_after=3)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
