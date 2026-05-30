import discord
from discord.ext import commands
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 💵 CORE ECONOMY
    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        await ctx.send(f"💰 **{target.name}'s Balance:**\nWallet: 0 | Bank: 0")

    @commands.command(name="work")
    async def work(self, ctx):
        await ctx.send("🛠️ You worked a shift and earned some cash!")

    @commands.command(name="daily")
    async def daily(self, ctx):
        await ctx.send("📅 You claimed your daily reward!")

    @commands.command(name="crime", aliases=["slut"])
    async def crime(self, ctx):
        await ctx.send("🥷 You attempted a crime... calculating payout or fine...")

    @commands.command(name="deposit")
    async def deposit(self, ctx, amount: str):
        await ctx.send(f"🏦 Deposited **{amount}** into your secure bank.")

    @commands.command(name="withdraw")
    async def withdraw(self, ctx, amount: str):
        await ctx.send(f"🏧 Withdrew **{amount}** from your bank.")

    # 🛒 SHOP & INVENTORY
    @commands.group(name="shop", invoke_without_command=True)
    async def shop(self, ctx):
        await ctx.send("🛒 **Server Shop:** (No items configured yet)")

    @commands.command(name="buy")
    async def buy(self, ctx, *, item_name: str):
        await ctx.send(f"🛍️ Attempting to purchase: {item_name}...")

    # 🎲 GAMBLING & GAMES
    @commands.command(name="slots")
    async def slots(self, ctx, bet: int):
        await ctx.send(f"🎰 Spinning the slot machine for **{bet}** coins...")

    @commands.command(name="roulette")
    async def roulette(self, ctx, color: str, bet: int):
        await ctx.send(f"🎡 Betting {bet} on {color}. Spinning the wheel...")

    @commands.command(name="blackjack")
    async def blackjack(self, ctx, bet: int):
        await ctx.send(f"🃏 Dealing cards for Blackjack... Bet: {bet}")

    # 🐸 FUN & ANIMALS
    @commands.command(name="meme")
    async def meme(self, ctx):
        await ctx.send("🐸 Fetching a fresh meme from Reddit...")

    @commands.command(name="pokemon")
    async def pokemon(self, ctx, name: str):
        await ctx.send(f"📱 Accessing Pokedex data for: **{name}**...")

    # ⚙️ ADMIN ECONOMY
    @commands.command(name="addmoney")
    @commands.has_permissions(administrator=True)
    async def addmoney(self, ctx, user: discord.Member, amount: int):
        await ctx.send(f"💸 Minted and added **{amount}** to {user.name}'s account.")

async def setup(bot):
    await bot.add_cog(Economy(bot))
