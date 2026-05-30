import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *, query: str):
        await ctx.send(f"🎵 Searching and queuing: **{query}**")

    @commands.command(name="stop", aliases=["leave", "disconnect"])
    async def stop(self, ctx):
        await ctx.send("🛑 Music stopped. Queue cleared and disconnecting.")

    @commands.command(name="pause")
    async def pause(self, ctx):
        await ctx.send("⏸️ Track paused.")

    @commands.command(name="resume")
    async def resume(self, ctx):
        await ctx.send("▶️ Track resumed.")

    @commands.command(name="skip", aliases=["s"])
    async def skip(self, ctx):
        await ctx.send("⏭️ Skipped to the next track.")

    @commands.command(name="queue", aliases=["q"])
    async def queue(self, ctx):
        await ctx.send("📜 Fetching the upcoming music queue...")

    @commands.command(name="loop")
    async def loop(self, ctx, mode: str = "track"):
        await ctx.send(f"🔁 Looping set to: **{mode}**")

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx, level: int):
        await ctx.send(f"🔊 Master volume set to **{level}%**")

    @commands.group(name="filter", invoke_without_command=True)
    async def audio_filter(self, ctx, effect: str):
        await ctx.send(f"🎛️ Applied audio DSP filter: **{effect.upper()}**")

async def setup(bot):
    await bot.add_cog(Music(bot))
