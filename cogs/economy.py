import discord
from discord.ext import commands
from discord import app_commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Temporary dictionary until we hook up PostgreSQL
        self.balances = {} 

    @app_commands.command(name="balance", description="Check your bank balance.")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        bal = self.balances.get(str(target.id), 0)
        await interaction.response.send_message(f"🏦 **{target.display_name}** currently has **${bal}**.")

    @app_commands.command(name="work", description="Work a virtual shift to earn cash.")
    @app_commands.checks.cooldown(1, 3600, key=lambda i: (i.user.id)) # 1 hour cooldown
    async def work(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        earned = random.randint(200, 800)
        
        current_bal = self.balances.get(user_id, 0)
        self.balances[user_id] = current_bal + earned
        
        await interaction.response.send_message(f"💼 You worked hard and earned **${earned}**! Your new balance is **${self.balances[user_id]}**.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
  
