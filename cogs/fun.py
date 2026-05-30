import discord
from discord.ext import commands
from discord import app_commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coinflip", description="Flips a virtual coin")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"🪙 The coin landed on: **{result}**")

    @app_commands.command(name="8ball", description="Ask the Magic 8-Ball a question")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = ["Yes, definitely.", "Without a doubt.", "Reply hazy, try again.", "Don't count on it.", "My sources say no."]
        await interaction.response.send_message(f"🎱 **Question:** {question}\n**Answer:** {random.choice(responses)}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
