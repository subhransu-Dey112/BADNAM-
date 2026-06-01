import discord
from discord.ext import commands
import datetime
import asyncio
import json
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}
        self.db_file = "mod_db.json"
        self._load_db()

    def _load_db(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump({"warns": {}, "jails": {}}, f)
        with open(self.db_file, "r") as f:
            self.db = json.load(f)

    def _save_db(self):
        with open(self.db_file, "w") as f:
            json.dump(self.db, f, indent=4)

    # ==========================================
    # 1. USER MODERATION (Kick, Ban, Mute, Nick)
    # ==========================================
    @commands.command(aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"✅ Kicked **{member.name}** | {reason}")

    @commands.command(aliases=["b"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned **{member.name}** | {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason="No reason"):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"✅ Unbanned **{user.name}**")

    @commands.command(aliases=["timeout"])
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="No reason"):
        duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await ctx.send(f"⏱️ Muted **{member.name}** for {minutes}m")

    @commands.command(aliases=["untimeout"])
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 Unmuted **{member.name}**")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, name: str):
        await member.edit(nick=name)
        await ctx.send(f"✅ Changed nickname to **{name}**")

    # ==========================================
    # 2. ROLE MANAGEMENT (Role, Roleall)
    # ==========================================
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        """Toggles a role on a user (Adds it if they don't have it, removes it if they do)"""
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"➖ Removed **{role.name}** from {member.mention}")
        else:
            await member.add_roles(role)
            await ctx.send(f"➕ Added **{role.name}** to {member.mention}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def roleall(self, ctx, role: discord.Role):
        """Gives a role to every human in the server (Takes time to avoid rate limits)"""
        msg = await ctx.send(f"🔄 Adding **{role.name}** to all humans. Please wait...")
        count = 0
        for member in ctx.guild.members:
            if not member.bot and role not in member.roles:
                try:
                    await member.add_roles(role)
                    count += 1
                    await asyncio.sleep(1) # CRITICAL: Prevents Discord from banning the bot for API spam
                except discord.Forbidden:
                    return await msg.edit(content="❌ I don't have permission! Make sure my role is higher than the role you are giving.")
        await msg.edit(content=f"✅ Successfully added **{role.name}** to {count} members.")

    # ==========================================
    # 3. CHANNEL SECURITY (Lock, Hide, Nuke)
    # ==========================================
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(f"🔒 Locked {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(f"🔓 Unlocked {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await ctx.send(f"👻 Hid {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unhide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        await ctx.send(f"👁️ Unhid {channel.mention}")

    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def nuke(self, ctx):
        pos = ctx.channel.position
        new_channel = await ctx.channel.clone()
        await ctx.channel.delete()
        await new_channel.edit(position=pos)
        await new_channel.send("☢️ Channel Nuked!")

    # ==========================================
    # 4. MASS SERVER ACTIONS (Lockall, Hideall)
    # ==========================================
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lockall(self, ctx):
        msg = await ctx.send("🔒 Locking all channels...")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await msg.edit(content="✅ Locked all text channels.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlockall(self, ctx):
        msg = await ctx.send("🔓 Unlocking all channels...")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await msg.edit(content="✅ Unlocked all text channels.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def hideall(self, ctx):
        msg = await ctx.send("👻 Hiding all channels...")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await msg.edit(content="✅ Hid all text channels.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unhideall(self, ctx):
        msg = await ctx.send("👁️ Unhiding all channels...")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.default_role, view_channel=True)
        await msg.edit(content="✅ Unhid all text channels.")

    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def unmuteall(self, ctx):
        """Unmutes everyone currently in your voice channel"""
        if not ctx.author.voice:
            return await ctx.send("❌ You must be in a Voice Channel to use this.")
        count = 0
        for member in ctx.author.voice.channel.members:
            if member.voice.mute:
                await member.edit(mute=False)
                count += 1
        await ctx.send(f"✅ Unmuted {count} members in VC.")

    # ==========================================
    # 5. PURGE SYSTEM
    # ==========================================
    @commands.group(invoke_without_command=True, aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"✅ Purged {amount} messages")
        await msg.delete(delay=3)

    @purge.command(name="user")
    @commands.has_permissions(manage_messages=True)
    async def purge_user(self, ctx, member: discord.Member, amount: int):
        def check(m): return m.author == member
        await ctx.channel.purge(limit=amount + 1, check=check)
        msg = await ctx.send(f"✅ Purged {amount} messages from {member.name}")
        await msg.delete(delay=3)

    # ==========================================
    # 6. WARNINGS (JSON DATABASE)
    # ==========================================
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="No reason"):
        uid = str(member.id)
        if uid not in self.db["warns"]: self.db["warns"][uid] = []
        self.db["warns"][uid].append(reason)
        self._save_db()
        await ctx.send(f"⚠️ Warned **{member.name}** | {reason}")

    @warn.command(name="list")
    @commands.has_permissions(moderate_members=True)
    async def warn_list(self, ctx, member: discord.Member):
        warns = self.db["warns"].get(str(member.id), [])
        if not warns: return await ctx.send("✅ This user has no warnings.")
        desc = "\n".join([f"{i+1}. {w}" for i, w in enumerate(warns)])
        await ctx.send(embed=discord.Embed(title=f"Warnings for {member.name}", description=desc, color=0xffcc00))

    @warn.command(name="clear")
    @commands.has_permissions(moderate_members=True)
    async def warn_clear(self, ctx, member: discord.Member):
        if str(member.id) in self.db["warns"]:
            del self.db["warns"][str(member.id)]
            self._save_db()
        await ctx.send(f"✅ Cleared all warnings for **{member.name}**")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
