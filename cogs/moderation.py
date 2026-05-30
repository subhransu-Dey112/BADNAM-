import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Permanently removes a user from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided."):
        try:
            await user.ban(reason=reason)
            await interaction.response.send_message(f"🔨 **{user.mention}** has been banned. Reason: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I do not have permission to ban this user.", ephemeral=True)

    @app_commands.command(name="kick", description="Forcibly removes a user from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided."):
        try:
            await user.kick(reason=reason)
            await interaction.response.send_message(f"👢 **{user.mention}** has been kicked. Reason: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I do not have permission to kick this user.", ephemeral=True)

    @app_commands.command(name="purge", description="Deletes a specified quantity of recent messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        # Defers the response so the bot has time to delete messages without the interaction failing
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"🧹 Successfully purged {len(deleted)} messages.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
