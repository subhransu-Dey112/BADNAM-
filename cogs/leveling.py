import discord
from discord.ext import commands
from discord import app_commands

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    level = app_commands.Group(name="level", description="Message leveling system")

    @level.command(name="enable", description="Enable the level system")
    @app_commands.checks.has_permissions(administrator=True)
    async def enable(self, interaction: discord.Interaction):
        await interaction.response.send_message("📈 **Leveling System Enabled.**")

    @app_commands.command(name="rank", description="Check a user's rank profile")
    async def rank(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        await interaction.response.send_message(f"📊 **{target.display_name}** is currently Level 1 (0 XP).")

async def setup(bot):
    await bot.add_cog(Leveling(bot))
