import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- PURGE COMMAND ---
    @commands.command(name="purge", aliases=["clear", "clean"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Deletes a specified number of messages."""
        # limit=amount+1 so it deletes the user's command message too
        deleted = await ctx.channel.purge(limit=amount + 1)
        # Sends a success message that automatically deletes itself after 3 seconds
        await ctx.send(f"✅ Successfully deleted {len(deleted)-1} messages.", delete_after=3)

    # --- KICK COMMAND ---
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kicks a member from the server."""
        if member == ctx.author:
            return await ctx.send("❌ You cannot kick yourself!")
            
        try:
            await member.kick(reason=reason)
            await ctx.send(f"👢 **{member.name}** has been kicked. | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to kick them! Make sure my Bot Role is higher than theirs.")

    # --- BAN COMMAND ---
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Bans a member from the server."""
        if member == ctx.author:
            return await ctx.send("❌ You cannot ban yourself!")
            
        try:
            await member.ban(reason=reason)
            await ctx.send(f"🔨 **{member.name}** has been banned. | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to ban them! Make sure my Bot Role is higher than theirs.")

    # --- TIMEOUT / MUTE COMMAND ---
    @commands.command(name="timeout", aliases=["mute"])
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
        """Mutes a member for a specified number of minutes."""
        try:
            # Converts the number of minutes into a format Discord understands
            duration = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            await ctx.send(f"⏱️ **{member.name}** has been muted for {minutes} minutes. | Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to mute them! Make sure my Bot Role is higher than theirs.")

    # --- ERROR HANDLING ---
    # This stops the bot from crashing in the console if a normal user tries to use a mod command
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have the required permissions to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ You are missing required arguments! Example: `{ctx.prefix}{ctx.command.name} @User`")

# This is required at the bottom of every cog file
async def setup(bot):
    await bot.add_cog(Moderation(bot))
