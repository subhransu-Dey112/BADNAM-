import discord
from discord.ext import commands
import json

# Simple JSON-based prefix storage
def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes.get(str(message.guild.id), 'b!')

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setprefix")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f"Prefix changed to `{prefix}`")

async def setup(bot):
    await bot.add_cog(Prefix(bot))
