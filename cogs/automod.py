import discord
from discord.ext import commands
from discord import app_commands

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = {}

    automod = app_commands.Group(name="automod", description="AutoMod settings")

    @automod.command(name="enable", description="Enables automod system")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def enable(self, interaction: discord.Interaction):
        self.config[str(interaction.guild.id)] = True
        await interaction.response.send_message("🤖 **AutoMod Enabled:** Now filtering chat.")

    @automod.command(name="disable", description="Disables automod system")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def disable(self, interaction: discord.Interaction):
        self.config[str(interaction.guild.id)] = False
        await interaction.response.send_message("🤖 **AutoMod Disabled.**")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
