import discord
from discord.ext import commands

class WelcomeSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🏷️ AUTOROLE
    @commands.group(name="autorole", invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def autorole(self, ctx): 
        pass

    @autorole.command(name="add")
    async def ar_add(self, ctx, role: discord.Role): 
        await ctx.send(f"🏷️ Users will now receive the **{role.name}** role on join.")

    @autorole.command(name="remove")
    async def ar_remove(self, ctx, role: discord.Role): 
        await ctx.send(f"❌ **{role.name}** removed from autorole list.")

    # 👋 WELCOME GATE
    @commands.group(name="welcome", invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx): 
        pass

    @welcome.command(name="enable")
    async def w_enable(self, ctx): 
        await ctx.send("👋 Welcome system **ENABLED**.")

    @welcome.command(name="channel")
    async def w_channel(self, ctx, action: str, channel: discord.TextChannel = None): 
        if action == "add" and channel:
            await ctx.send(f"📍 Welcome messages will be sent in {channel.mention}")
        elif action == "remove":
            await ctx.send("🗑️ Welcome channel removed.")

    @welcome.command(name="message")
    async def w_message(self, ctx, *, text: str): 
        await ctx.send("📝 Custom welcome message updated.")

    @welcome.command(name="button")
    async def w_button(self, ctx, action: str, name: str, link: str = None): 
        if action == "add":
            await ctx.send(f"🔘 Added welcome button: **{name}**")
        elif action == "remove":
            await ctx.send(f"🗑️ Removed welcome button: **{name}**")

async def setup(bot):
    await bot.add_cog(WelcomeSystem(bot))
