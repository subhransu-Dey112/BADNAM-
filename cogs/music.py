import discord
from discord.ext import commands
from discord import app_commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="play", description="Play a song in your voice channel")
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.send_message(f"🎵 Searching and queuing: **{query}**")

    @app_commands.command(name="stop", description="Stop the music and leave")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.send_message("⏹️ Music stopped. Disconnected.")

async def setup(bot):
    await bot.add_cog(Music(bot))
