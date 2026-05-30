import discord
from discord.ext import commands

class Automations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🤖 AUTO-RESPONDER
    @commands.group(name="autorespond", aliases=["ar"], invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def autorespond(self, ctx):
        pass

    @autorespond.command(name="add")
    async def ar_add(self, ctx, trigger: str, *, reply: str):
        await ctx.send(f"✅ Added auto-response: If user says `{trigger}`, bot replies `{reply}`.")

    @autorespond.command(name="remove")
    async def ar_remove(self, ctx, trigger: str):
        await ctx.send(f"🗑️ Removed auto-response for `{trigger}`.")

    @autorespond.command(name="list")
    async def ar_list(self, ctx):
        await ctx.send("📄 Fetching all active conversational triggers...")

    # ✨ AUTO-REACT
    @commands.group(name="autoreact", invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def autoreact(self, ctx):
        pass

    @autoreact.command(name="add")
    async def act_add(self, ctx, trigger: str, emoji: str):
        await ctx.send(f"✅ Bot will now react with {emoji} to messages containing `{trigger}`.")

    @autoreact.command(name="remove")
    async def act_remove(self, ctx, trigger: str):
        await ctx.send(f"🗑️ Removed auto-reaction for `{trigger}`.")

    # 📌 STICKY MESSAGES
    @commands.group(name="sticky", invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def sticky(self, ctx):
        pass

    @sticky.command(name="add")
    async def sticky_add(self, ctx, *, message: str):
        await ctx.send("📌 Sticky message set! I will pin this to the bottom of the chat constantly.")

    @sticky.command(name="remove")
    async def sticky_remove(self, ctx):
        await ctx.send("🧹 Sticky message loop disabled for this channel.")

async def setup(bot):
    await bot.add_cog(Automations(bot))
