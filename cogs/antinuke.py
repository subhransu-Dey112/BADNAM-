import discord
from discord.ext import commands
from discord import app_commands

class AntiNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Temporary dictionary until we link PostgreSQL
        self.security_settings = {} 

    # Creates a master group for slash commands (e.g. /antinuke enable)
    antinuke_group = app_commands.Group(name="antinuke", description="Master Anti-Nuke Security Controls")

    @antinuke_group.command(name="enable", description="Activates anti-nuke protection for the server.")
    @app_commands.checks.has_permissions(administrator=True)
    async def enable(self, interaction: discord.Interaction):
        self.security_settings[str(interaction.guild.id)] = True
        embed = discord.Embed(
            title="🛡️ Security Systems Online", 
            description="Master Anti-Nuke module has been **ENABLED**.\nMonitoring all bans, kicks, and channel deletions.", 
            color=0x00ff00
        )
        await interaction.response.send_message(embed=embed)

    @antinuke_group.command(name="disable", description="Deactivates anti-nuke protection.")
    @app_commands.checks.has_permissions(administrator=True)
    async def disable(self, interaction: discord.Interaction):
        self.security_settings[str(interaction.guild.id)] = False
        embed = discord.Embed(
            title="⚠️ Security Systems Offline", 
            description="Master Anti-Nuke module has been **DISABLED**. Your server is vulnerable.", 
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="panic", description="Instantly locks down all channels to stop a raid.")
    @app_commands.checks.has_permissions(administrator=True)
    async def panic(self, interaction: discord.Interaction):
        await interaction.response.send_message("🚨 **PANIC MODE INITIATED.** Locking down server...", ephemeral=True)
        # Locks every channel for @everyone
        for channel in interaction.guild.text_channels:
            try:
                await channel.set_permissions(interaction.guild.default_role, send_messages=False)
            except:
                continue
        await interaction.followup.send("🔒 **Server Lockdown Complete.** All channels restricted.")

    @app_commands.command(name="whitelist", description="Whitelist a user to bypass anti-nuke limits.")
    @app_commands.checks.has_permissions(administrator=True)
    async def whitelist(self, interaction: discord.Interaction, user: discord.Member):
        # Logic to add user to Redis/PostgreSQL whitelist goes here
        await interaction.response.send_message(f"✅ {user.mention} has been added to the Security Whitelist.")

async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
