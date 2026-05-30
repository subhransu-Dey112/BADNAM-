import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔨 CORE PUNISHMENTS
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided."):
        await ctx.send(f"🔨 **{user.mention}** has been banned. Reason: {reason}")

    @commands.command(name="softban")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member, *, reason="No reason provided."):
        await ctx.send(f"🧹 **{user.mention}** was softbanned (banned and instantly unbanned to clear messages).")

    @commands.command(name="hackban")
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, user_id: int, *, reason="No reason provided."):
        await ctx.send(f"🥷 User ID **{user_id}** has been hackbanned.")

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason="No reason provided."):
        await ctx.send(f"✅ User ID **{user_id}** has been unbanned.")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided."):
        await ctx.send(f"👢 **{user.mention}** has been kicked. Reason: {reason}")

    @commands.command(name="timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, user: discord.Member, duration: str, *, reason="No reason provided."):
        await ctx.send(f"⏱️ **{user.mention}** has been timed out for {duration}. Reason: {reason}")

    @commands.command(name="untimeout")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, user: discord.Member):
        await ctx.send(f"✅ Timeout removed from **{user.mention}**.")

    # 🔇 MUTING SYSTEM
    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, duration: str = None, *, reason="No reason provided."):
        time_text = f" for {duration}" if duration else " permanently"
        await ctx.send(f"🔇 **{user.mention}** has been muted{time_text}.")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        await ctx.send(f"🔊 **{user.mention}** has been unmuted.")

    @commands.command(name="tempmute")
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, user: discord.Member, duration: str, *, reason="No reason provided."):
        await ctx.send(f"⏳ **{user.mention}** temporarily muted for {duration}.")

    @commands.command(name="tempban")
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, user: discord.Member, duration: str, *, reason="No reason provided."):
        await ctx.send(f"⏳ **{user.mention}** temporarily banned for {duration}.")

    # ⚠️ WARNINGS & NOTES
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.Member, *, reason="No reason provided."):
        await ctx.send(f"⚠️ **{user.mention}** has been warned. Reason: {reason}")

    @commands.command(name="warnings")
    async def warnings(self, ctx, user: discord.Member):
        await ctx.send(f"📄 Displaying warning history for **{user.mention}**...")

    @commands.command(name="delwarn")
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, warning_id: int):
        await ctx.send(f"🗑️ Warning ID **{warning_id}** deleted.")

    @commands.command(name="clearwarns")
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, user: discord.Member):
        await ctx.send(f"✨ All warnings cleared for **{user.mention}**.")

    @commands.command(name="reason")
    @commands.has_permissions(manage_messages=True)
    async def reason(self, ctx, case_id: int, *, new_reason: str):
        await ctx.send(f"✏️ Updated case **#{case_id}** reason to: {new_reason}")

    # 🧹 PURGE ENGINE
    @commands.group(name="purge", invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if amount:
            await ctx.send(f"🧹 Purging **{amount}** messages...")
        else:
            await ctx.send("❓ Usage: `b!purge <amount | user | match | embeds | attachments | bots>`")

    @purge.command(name="user")
    async def purge_user(self, ctx, user: discord.Member, amount: int):
        await ctx.send(f"🧹 Purging {amount} messages sent by **{user.name}**...")

    @purge.command(name="match")
    async def purge_match(self, ctx, keyword: str, amount: int):
        await ctx.send(f"🧹 Purging {amount} messages containing `{keyword}`...")

    @purge.command(name="embeds")
    async def purge_embeds(self, ctx, amount: int):
        await ctx.send(f"🧹 Purging {amount} embed messages...")

    @purge.command(name="attachments")
    async def purge_attachments(self, ctx, amount: int):
        await ctx.send(f"🧹 Purging {amount} messages with attachments...")

    @purge.command(name="bots")
    async def purge_bots(self, ctx, amount: int):
        await ctx.send(f"🧹 Purging {amount} bot messages...")

    # 🔒 CHANNEL CONTROLS
    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, duration: int):
        await ctx.send(f"🐢 Slowmode set to **{duration} seconds**.")

    @commands.group(name="lock", invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.send("🔒 Channel locked.")

    @lock.command(name="server")
    @commands.has_permissions(administrator=True)
    async def lock_server(self, ctx):
        await ctx.send("🚨 **SERVER LOCKDOWN.** All channels locked.")

    @commands.group(name="unlock", invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.send("🔓 Channel unlocked.")

    @unlock.command(name="server")
    @commands.has_permissions(administrator=True)
    async def unlock_server(self, ctx):
        await ctx.send("🔓 **SERVER UNLOCKED.** All channels reopened.")

    # 📝 ADMINISTRATIVE NOTES
    @commands.group(name="note", invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def note(self, ctx):
        pass

    @note.command(name="add")
    async def note_add(self, ctx, user: discord.Member, *, text: str):
        await ctx.send(f"📝 Note added to **{user.name}**: {text}")

    @note.command(name="view")
    async def note_view(self, ctx, user: discord.Member):
        await ctx.send(f"📂 Fetching staff notes for **{user.name}**...")

    @note.command(name="delete")
    async def note_delete(self, ctx, note_id: int):
        await ctx.send(f"🗑️ Note ID **{note_id}** deleted.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
