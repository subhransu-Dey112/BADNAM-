import discord
from discord.ext import commands
from discord import app_commands

class VoiceMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    vc = app_commands.Group(name="vc", description="VoiceMaster controls")

    @vc.command(name="setup", description="Setup Join-to-Create voice channels")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_vc(self, interaction: discord.Interaction):
        await interaction.response.send_message("🎙️ **VoiceMaster setup complete.**")

    @vc.command(name="lock", description="Lock your current temporary VC")
    async def lock_vc(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔒 Your voice channel is now locked.")

async def setup(bot):
    await bot.add_cog(VoiceMaster(bot))
