import discord
from discord.ext import commands
import asyncio

class MassRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # This dictionary will let us stop the process if we need to
        self.active_processes = {}

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def roleall(self, ctx, role: discord.Role = None):
        if not role:
            return await ctx.send("❌ Please provide a role. Usage: `b!roleall [@role]`")
        
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send("❌ I cannot assign a role that is higher than my own highest role!")

        # Count how many humans actually need the role
        members_to_role = [m for m in ctx.guild.members if not m.bot and role not in m.roles]
        
        if not members_to_role:
            return await ctx.send(f"✅ All humans already have the **{role.name}** role!")

        msg = await ctx.send(f"⏳ **Starting Mass Role:** Giving **{role.name}** to {len(members_to_role)} members...\n*(Type `b!stoprole` to cancel)*")
        self.active_processes[ctx.guild.id] = True

        success = 0
        failed = 0

        for member in members_to_role:
            if not self.active_processes.get(ctx.guild.id, False):
                return await ctx.send("🛑 **Mass Role Operation Cancelled!**")
            
            try:
                await member.add_roles(role)
                success += 1
            except:
                failed += 1
            
            # CRITICAL: 1 second delay to prevent Discord API bans
            await asyncio.sleep(1)

        self.active_processes[ctx.guild.id] = False
        await msg.edit(content=f"✅ **Mass Role Complete!**\nSuccessfully added to: `{success}`\nFailed: `{failed}`")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unroleall(self, ctx, role: discord.Role = None):
        if not role:
            return await ctx.send("❌ Please provide a role. Usage: `b!unroleall [@role]`")
        
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send("❌ I cannot remove a role that is higher than my own highest role!")

        # Count how many humans actually have the role
        members_to_unrole = [m for m in ctx.guild.members if not m.bot and role in m.roles]
        
        if not members_to_unrole:
            return await ctx.send(f"✅ No humans currently have the **{role.name}** role.")

        msg = await ctx.send(f"⏳ **Starting Mass Un-Role:** Removing **{role.name}** from {len(members_to_unrole)} members...\n*(Type `b!stoprole` to cancel)*")
        self.active_processes[ctx.guild.id] = True

        success = 0
        failed = 0

        for member in members_to_unrole:
            if not self.active_processes.get(ctx.guild.id, False):
                return await ctx.send("🛑 **Mass Un-Role Operation Cancelled!**")
            
            try:
                await member.remove_roles(role)
                success += 1
            except:
                failed += 1
            
            # CRITICAL: 1 second delay to prevent Discord API bans
            await asyncio.sleep(1)

        self.active_processes[ctx.guild.id] = False
        await msg.edit(content=f"✅ **Mass Un-Role Complete!**\nSuccessfully removed from: `{success}`\nFailed: `{failed}`")

    @commands.command(name="stoprole")
    @commands.has_permissions(administrator=True)
    async def stop_role(self, ctx):
        if self.active_processes.get(ctx.guild.id, False):
            self.active_processes[ctx.guild.id] = False
            await ctx.send("🛑 Stopping the active role operation... (It will halt on the next member).")
        else:
            await ctx.send("❌ There are no active mass-role operations running right now.")

async def setup(bot):
    await bot.add_cog(MassRoles(bot))
