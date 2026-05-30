import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🎁 GIVEAWAYS
    @commands.group(name="giveaway", aliases=["gw"], invoke_without_command=True)
    @commands.has_permissions(manage_events=True)
    async def giveaway(self, ctx):
        pass

    @giveaway.command(name="start")
    async def gw_start(self, ctx, duration: str, winners: int, *, prize: str):
        await ctx.send(f"🎉 Giveaway started for **{prize}**! Ends in {duration}.")

    @giveaway.command(name="reroll")
    async def gw_reroll(self, ctx, message_id: int):
        await ctx.send("🎲 Rerolling giveaway winner...")

    # ⭐ STARBOARD & SUGGESTIONS
    @commands.command(name="starboard")
    @commands.has_permissions(administrator=True)
    async def starboard(self, ctx, action: str):
        await ctx.send(f"⭐ Starboard system: **{action.upper()}**")

    @commands.command(name="suggest")
    async def suggest(self, ctx, *, idea: str):
        await ctx.send("💡 Suggestion submitted successfully!")

    @commands.group(name="suggestion", invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def mod_suggestion(self, ctx):
        pass

    @mod_suggestion.command(name="approve")
    async def sugg_approve(self, ctx, msg_id: int, *, reason: str = "Great idea!"):
        await ctx.send(f"✅ Suggestion {msg_id} approved: {reason}")

async def setup(bot):
    await bot.add_cog(Events(bot))
