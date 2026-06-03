import discord
from discord.ext import commands
import json
import os

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "security_db.json"
        self._load_db()

    def _load_db(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f: json.dump({}, f)
        with open(self.db_file, "r") as f: self.db = json.load(f)

    def _save_db(self):
        with open(self.db_file, "w") as f: json.dump(self.db, f, indent=4)

    def get_data(self, guild_id):
        gid = str(guild_id)
        if gid not in self.db:
            self.db[gid] = {
                "q_role": None,
                "q_log": None,
                "extra_owners": [],
                "permit_owner": [],
                "ignore_cmds": [],
                "ignore_chans": [],
                "ignore_users": [],
                "ignore_bypass": []
            }
        return self.db[gid]

    # ==========================================
    # 🦠 QUARANTINE SYSTEM
    # ==========================================
    @commands.group(name="quarantinerole", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def q_role(self, ctx):
        await ctx.send("Use `create`, `set`, `reset`, `show`")

    @q_role.command(name="create")
    @commands.has_permissions(administrator=True)
    async def q_role_create(self, ctx):
        try:
            role = await ctx.guild.create_role(name="Quarantined", color=discord.Color.dark_grey(), reason="Quarantine Setup")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False, add_reactions=False, speak=False)
            self.get_data(ctx.guild.id)["q_role"] = role.id
            self._save_db()
            await ctx.send(f"✅ Created and set quarantine role: {role.mention}")
        except discord.Forbidden:
            await ctx.send("❌ I lack permissions to create roles.")

    @q_role.command(name="set")
    @commands.has_permissions(administrator=True)
    async def q_role_set(self, ctx, role: discord.Role):
        self.get_data(ctx.guild.id)["q_role"] = role.id
        self._save_db()
        await ctx.send(f"✅ Quarantine role set to {role.mention}")

    @q_role.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def q_role_reset(self, ctx):
        self.get_data(ctx.guild.id)["q_role"] = None
        self._save_db()
        await ctx.send("✅ Quarantine role cleared.")

    @q_role.command(name="show")
    @commands.has_permissions(administrator=True)
    async def q_role_show(self, ctx):
        r = self.get_data(ctx.guild.id)["q_role"]
        await ctx.send(f"🦠 Quarantine Role: <@&{r}>" if r else "❌ No quarantine role set.")

    @commands.group(name="quarantinelog", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def q_log(self, ctx):
        pass

    @q_log.command(name="set")
    @commands.has_permissions(administrator=True)
    async def q_log_set(self, ctx, channel: discord.TextChannel):
        self.get_data(ctx.guild.id)["q_log"] = channel.id
        self._save_db()
        await ctx.send(f"✅ Quarantine logs set to {channel.mention}")

    @q_log.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def q_log_reset(self, ctx):
        self.get_data(ctx.guild.id)["q_log"] = None
        self._save_db()
        await ctx.send("✅ Quarantine logs cleared.")

    @q_log.command(name="show")
    @commands.has_permissions(administrator=True)
    async def q_log_show(self, ctx):
        c = self.get_data(ctx.guild.id)["q_log"]
        await ctx.send(f"📡 Quarantine Log: <#{c}>" if c else "❌ No log channel set.")

    @commands.command(name="quarantine")
    @commands.has_permissions(manage_roles=True)
    async def quarantine_user(self, ctx, member: discord.Member):
        data = self.get_data(ctx.guild.id)
        if not data["q_role"]: return await ctx.send("❌ No quarantine role set! Use `b!quarantinerole set`")
        
        role = ctx.guild.get_role(data["q_role"])
        if role:
            await member.add_roles(role)
           @commands.group(name="extraowner", aliases=["permitextraowner"], invoke_without_command=True)
            if data["q_log"]:
                log_ch = ctx.guild.get_channel(data["q_log"])
                if log_ch: await log_ch.send(f"🔒 {member.mention} was quarantined by {ctx.author.mention}.")

    # ==========================================
    # 👑 PERMIT & EXTRA OWNER
    # ==========================================
    @commands.group(name="permission", aliases=["permit"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def permit_base(self, ctx, role: discord.Role = None):
        if role:
            is_owner = role.id in self.get_data(ctx.guild.id)["permit_owner"]
            await ctx.send(f"🛡️ **{role.name}** Permissions:\nOwner Permit: **{'✅' if is_owner else '❌'}**")
        else:
            await ctx.send("Use `b!permission @role`, `owner @role`, `reset @role`, `reset all`")

    @permit_base.command(name="owner")
    @commands.has_permissions(administrator=True)
    async def permit_owner(self, ctx, role: discord.Role):
        data = self.get_data(ctx.guild.id)
        if role.id not in data["permit_owner"]: data["permit_owner"].append(role.id)
        self._save_db()
        await ctx.send(f"👑 Added {role.mention} to Owner Permits.")

    @permit_base.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def permit_reset(self, ctx, target: str = None):
        data = self.get_data(ctx.guild.id)
        if target and target.lower() == "all":
            data["permit_owner"] = []
            await ctx.send("✅ All permits reset.")
        elif len(ctx.message.role_mentions) > 0:
            role = ctx.message.role_mentions[0]
            if role.id in data["permit_owner"]: data["permit_owner"].remove(role.id)
            await ctx.send(f"✅ Reset permits for {role.name}.")
        self._save_db()

    @commands.group(name="extraowner", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def extraowner(self, ctx):
        pass

    @extraowner.command(name="set")
    @commands.has_permissions(administrator=True)
    async def eo_set(self, ctx, user: discord.Member):
        data = self.get_data(ctx.guild.id)
        if user.id not in data["extra_owners"]: data["extra_owners"].append(user.id)
        self._save_db()
        await ctx.send(f"👑 {user.mention} is now an Extra Owner.")

    @extraowner.command(name="view", aliases=["show", "list"])
    @commands.has_permissions(administrator=True)
    async def eo_view(self, ctx):
        owners = [f"<@{u}>" for u in self.get_data(ctx.guild.id)["extra_owners"]]
        await ctx.send(embed=discord.Embed(title="👑 Extra Owners", description="\n".join(owners) if owners else "None", color=0x2b2d31))

    @extraowner.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def eo_reset(self, ctx):
        self.get_data(ctx.guild.id)["extra_owners"] = []
        self._save_db()
        await ctx.send("✅ All Extra Owners cleared.")

    # ==========================================
    # 🚫 IGNORE SYSTEM
    # ==========================================
    @commands.group(name="ignore", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def ignore_base(self, ctx):
        await ctx.send("Use `b!ignore [command/channel/user/bypass] [add/remove/show]`")

    # Command Ignore
    @ignore_base.group(name="command", invoke_without_command=True)
    async def ig_cmd(self, ctx): pass
    @ig_cmd.command(name="add")
    async def ig_cmd_add(self, ctx, cmd: str):
        self.get_data(ctx.guild.id)["ignore_cmds"].append(cmd.lower())
        self._save_db(); await ctx.send(f"✅ Ignoring command: `{cmd}`")
    @ig_cmd.command(name="remove")
    async def ig_cmd_remove(self, ctx, cmd: str):
        if cmd.lower() in self.get_data(ctx.guild.id)["ignore_cmds"]:
            self.get_data(ctx.guild.id)["ignore_cmds"].remove(cmd.lower())
            self._save_db(); await ctx.send(f"❌ Un-ignoring command: `{cmd}`")
    @ig_cmd.command(name="show")
    async def ig_cmd_show(self, ctx):
        await ctx.send(f"🚫 Ignored Commands: {', '.join(self.get_data(ctx.guild.id)['ignore_cmds']) or 'None'}")

    # Channel Ignore
    @ignore_base.group(name="channel", invoke_without_command=True)
    async def ig_chan(self, ctx): pass
    @ig_chan.command(name="add")
    async def ig_chan_add(self, ctx, ch: discord.TextChannel):
        self.get_data(ctx.guild.id)["ignore_chans"].append(ch.id)
        self._save_db(); await ctx.send(f"✅ Ignoring channel: {ch.mention}")
    @ig_chan.command(name="remove")
    async def ig_chan_remove(self, ctx, ch: discord.TextChannel):
        if ch.id in self.get_data(ctx.guild.id)["ignore_chans"]:
            self.get_data(ctx.guild.id)["ignore_chans"].remove(ch.id)
            self._save_db(); await ctx.send(f"❌ Un-ignoring channel: {ch.mention}")
    @ig_chan.command(name="show")
    async def ig_chan_show(self, ctx):
        chs = [f"<#{c}>" for c in self.get_data(ctx.guild.id)["ignore_chans"]]
        await ctx.send(f"🚫 Ignored Channels: {', '.join(chs) or 'None'}")

    # User Ignore
    @ignore_base.group(name="user", invoke_without_command=True)
    async def ig_user(self, ctx): pass
    @ig_user.command(name="add")
    async def ig_user_add(self, ctx, u: discord.Member):
        self.get_data(ctx.guild.id)["ignore_users"].append(u.id)
        self._save_db(); await ctx.send(f"✅ Ignoring user: {u.mention}")
    @ig_user.command(name="remove")
    async def ig_user_remove(self, ctx, u: discord.Member):
        if u.id in self.get_data(ctx.guild.id)["ignore_users"]:
            self.get_data(ctx.guild.id)["ignore_users"].remove(u.id)
            self._save_db(); await ctx.send(f"❌ Un-ignoring user: {u.mention}")
    @ig_user.command(name="show")
    async def ig_user_show(self, ctx):
        usrs = [f"<@{u}>" for u in self.get_data(ctx.guild.id)["ignore_users"]]
        await ctx.send(f"🚫 Ignored Users: {', '.join(usrs) or 'None'}")

    # Bypass Ignore
    @ignore_base.group(name="bypass", invoke_without_command=True)
    async def ig_byp(self, ctx): pass
    @ig_byp.command(name="add")
    async def ig_byp_add(self, ctx, r: discord.Role):
        self.get_data(ctx.guild.id)["ignore_bypass"].append(r.id)
        self._save_db(); await ctx.send(f"✅ {r.mention} now bypasses ignores.")
    @ig_byp.command(name="remove")
    async def ig_byp_remove(self, ctx, r: discord.Role):
        if r.id in self.get_data(ctx.guild.id)["ignore_bypass"]:
            self.get_data(ctx.guild.id)["ignore_bypass"].remove(r.id)
            self._save_db(); await ctx.send(f"❌ Removed bypass for {r.mention}.")
    @ig_byp.command(name="show")
    async def ig_byp_show(self, ctx):
        byp = [f"<@&{b}>" for b in self.get_data(ctx.guild.id)["ignore_bypass"]]
        await ctx.send(f"🛡️ Ignore Bypasses: {', '.join(byp) or 'None'}")

async def setup(bot):
    await bot.add_cog(Security(bot))
