import discord
from discord.ext import commands
from discord import app_commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ticket = app_commands.Group(name="ticket", description="Ticket system settings")

    @ticket.command(name="setup", description="Enable the ticket system")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message("🎫 Ticket panel deployed.")
        # We will add the actual interactive button logic here later

    @ticket.command(name="close", description="Close the current ticket")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def close_ticket(self, interaction: discord.Interaction):
        if "ticket-" in interaction.channel.name:
            await interaction.response.send_message("Closing ticket in 3 seconds...")
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("❌ This is not a ticket channel.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
