import discord
from discord.ext import commands
import json
import os

class AntiNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "antinuke_db.json"
        self._load_db()

    def _load_db(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump({}, f)
        with open(self.db_file, "r") as f:
            self.db = json.load(f)

    def _save_db(self):
        with open(self.db_file, "w") as f:
            json.dump(self.db, f, indent=4)

    def get_data(self, guild_id):
        gid = str(guild_id)
        if gid not in self.db:
            self.db[gid] = {
                "enabled": False,
                "log_channel": None,
                "log_msg": "🚨 Anti-Nuke Alert!",
                "whitelist": [],
                "extra_owners": []
            }
        return self.db[gid]

    async def log_action(self, guild, message):
        data = self.get_data(guild.id)
        if data["log_channel"]:
            log_chan = guild.get_channel(data["log_channel"])
            if log_chan:
                await log_chan.send(f"{data['log_msg']}\n{message}")

    def is_authorized(self, user, guild):
        data = self.get_data(guild.id)
        if user.id == self.bot.user.id or user.id == guild.owner_id: return True
        if user.id in data["whitelist"] or user.id in data["extra_owners"]: return True
        return False

    # ==========================================
    # PART 1: SETTINGS & COMMANDS
    # ==========================================
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antinuke(self, ctx):
        await ctx.send("Use `b!antinuke enable` or `b!antinuke disable`")

    @antinuke.command(name="enable")
    @commands.has_permissions(administrator=True)
    async def an_enable(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["enabled"] = True
        self._save_db()
        await ctx.send("✅ **Anti-Nuke is now ENABLED.**")

    @antinuke.command(name="disable")
    @commands.has_permissions(administrator=True)
    async def an_disable(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["enabled"] = False
        self._save_db()
        await ctx.send("❌ **Anti-Nuke is now DISABLED.**")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antinukelog(self, ctx):
        pass

    @antinukelog.command(name="set")
    @commands.has_permissions(administrator=True)
    async def log_set(self, ctx, channel: discord.TextChannel):
        data = self.get_data(ctx.guild.id)
        data["log_channel"] = channel.id
        self._save_db()
        await ctx.send(f"✅ Logs set to {channel.mention}")

    @antinukelog.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def log_reset(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["log_channel"] = None
        self._save_db()
        await ctx.send("✅ Log channel reset.")

    @antinukelog.command(name="show")
    @commands.has_permissions(administrator=True)
    async def log_show(self, ctx):
        data = self.get_data(ctx.guild.id)
        if data["log_channel"]: await ctx.send(f"📡 Current log channel: <#{data['log_channel']}>")
        else: await ctx.send("❌ No log channel set.")

    @antinukelog.command(name="msg")
    @commands.has_permissions(administrator=True)
    async def log_msg(self, ctx, *, message: str):
        data = self.get_data(ctx.guild.id)
        data["log_msg"] = message
        self._save_db()
        await ctx.send(f"✅ Log message updated to: `{message}`")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, member: discord.Member = None):
        if member:
            data = self.get_data(ctx.guild.id)
            if member.id not in data["whitelist"]:
                data["whitelist"].append(member.id)
                self._save_db()
                await ctx.send(f"✅ **{member.name}** is whitelisted.")
        else: await ctx.send("Use `b!whitelist @user`, `remove`, `show`, or `resetall`")

    @whitelist.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def wl_remove(self, ctx, member: discord.Member):
        data = self.get_data(ctx.guild.id)
        if member.id in data["whitelist"]:
            data["whitelist"].remove(member.id)
            self._save_db()
            await ctx.send(f"❌ **{member.name}** removed from whitelist.")

    @whitelist.command(name="show")
    @commands.has_permissions(administrator=True)
    async def wl_show(self, ctx):
        data = self.get_data(ctx.guild.id)
        if not data["whitelist"]: return await ctx.send("📋 Whitelist is empty.")
        users = [f"<@{uid}>" for uid in data["whitelist"]]
        await ctx.send(embed=discord.Embed(title="🛡️ Whitelist", description="\n".join(users), color=0x2b2d31))

    @whitelist.command(name="resetall")
    @commands.has_permissions(administrator=True)
    async def wl_resetall(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["whitelist"] = []
        self._save_db()
        await ctx.send("✅ Whitelist completely cleared.")

    @commands.group(invoke_without_command=True)
    async def extraowner(self, ctx):
        pass

    @extraowner.command(name="set")
    async def eo_set(self, ctx, member: discord.Member):
        if ctx.author.id != ctx.guild.owner_id: return await ctx.send("❌ Only the Server Owner can use this.")
        data = self.get_data(ctx.guild.id)
        if member.id not in data["extra_owners"]:
            data["extra_owners"].append(member.id)
            self._save_db()
            await ctx.send(f"👑 **{member.name}** is now an Extra Owner.")

    @extraowner.command(name="remove")
    async def eo_remove(self, ctx, member: discord.Member):
        if ctx.author.id != ctx.guild.owner_id: return await ctx.send("❌ Only the Server Owner can use this.")
        data = self.get_data(ctx.guild.id)
        if member.id in data["extra_owners"]:
            data["extra_owners"].remove(member.id)
            self._save_db()
            await ctx.send(f"❌ **{member.name}** removed from Extra Owners.")

    @extraowner.command(name="list")
    async def eo_list(self, ctx):
        data = self.get_data(ctx.guild.id)
        if not data["extra_owners"]: return await ctx.send("📋 No extra owners set.")
        users = [f"<@{uid}>" for uid in data["extra_owners"]]
        await ctx.send(embed=discord.Embed(title="👑 Extra Owners", description="\n".join(users), color=0x2b2d31))

    @extraowner.command(name="reset")
    async def eo_reset(self, ctx):
        if ctx.author.id != ctx.guild.owner_id: return await ctx.send("❌ Only the Server Owner can use this.")
        data = self.get_data(ctx.guild.id)
        data["extra_owners"] = []
        self._save_db()
        await ctx.send("✅ Extra Owners reset.")

    # ==========================================
    # PART 2: THE TRIGGERS (Auto-Bans)
    # ==========================================
    
    # 🛑 Anti-Channel Delete
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        data = self.get_data(channel.guild.id)
        if not data["enabled"]: return

        async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            if self.is_authorized(entry.user, channel.guild): return
            
            try:
                await channel.guild.ban(entry.user, reason="Anti-Nuke: Unauthorized Channel Deletion")
                await channel.clone(reason="Anti-Nuke: Channel Restored")
                await self.log_action(channel.guild, f"🔨 Banned **{entry.user.name}** for deleting a channel.\n♻️ The channel was restored.")
            except: pass

    # 🛑 Anti-Mass Ban
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        data = self.get_data(guild.id)
        if not data["enabled"]: return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if self.is_authorized(entry.user, guild): return
            
            try:
                await guild.ban(entry.user, reason="Anti-Nuke: Unauthorized Ban")
                await guild.unban(user, reason="Anti-Nuke: Reverting rogue ban")
                await self.log_action(guild, f"🔨 Banned **{entry.user.name}** for rogue banning.\n♻️ Unbanned their victim.")
            except: pass

    # 🛑 Anti-Role Delete
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        data = self.get_data(role.guild.id)
        if not data["enabled"]: return

        async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            if self.is_authorized(entry.user, role.guild): return
            
            try:
                await role.guild.ban(entry.user, reason="Anti-Nuke: Unauthorized Role Deletion")
                await role.guild.create_role(name=role.name, permissions=role.permissions, color=role.color, reason="Anti-Nuke: Role Restored")
                await self.log_action(role.guild, f"🔨 Banned **{entry.user.name}** for deleting a role.\n♻️ The role was restored.")
            except: pass

async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
