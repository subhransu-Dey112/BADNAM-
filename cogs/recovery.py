import discord
from discord.ext import commands
import json
import os
import asyncio
import aiohttp

class Recovery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "recovery_config.json"
        self.tokens_file = "oauth_tokens.json"
        self.snapshot_file = "server_snapshots.json"
        self.pulling_active = False
        self._load_dbs()

    def _load_dbs(self):
        for file in [self.config_file, self.tokens_file, self.snapshot_file]:
            if not os.path.exists(file):
                with open(file, "w") as f: json.dump({}, f)
                
        with open(self.config_file, "r") as f: self.config = json.load(f)
        with open(self.tokens_file, "r") as f: self.tokens = json.load(f)
        with open(self.snapshot_file, "r") as f: self.snapshots = json.load(f)

    def _save_db(self, db_type):
        if db_type == "config":
            with open(self.config_file, "w") as f: json.dump(self.config, f, indent=4)
        elif db_type == "tokens":
            with open(self.tokens_file, "w") as f: json.dump(self.tokens, f, indent=4)
        elif db_type == "snapshot":
            with open(self.snapshot_file, "w") as f: json.dump(self.snapshots, f, indent=4)

    def get_guild_config(self, guild_id):
        gid = str(guild_id)
        if gid not in self.config:
            self.config[gid] = {
                "verify_channel": None,
                "verify_role": None,
                "logs_channel": None,
                "whitelist": [],
                "blacklist": []
            }
        return self.config[gid]

    def is_allowed(self, ctx):
        if ctx.author.guild_permissions.administrator: return True
        cfg = self.get_guild_config(ctx.guild.id)
        return ctx.author.id in cfg["whitelist"]

    # ==========================================
    # 🔗 CONFIGURATION & VERIFICATION SETUP
    # ==========================================
    @commands.group(name="auth", invoke_without_command=True)
    async def auth_group(self, ctx):
        if not self.is_allowed(ctx): return
        await ctx.send("⚙️ **Auth Commands:** `b!auth channel`, `b!auth role`, `b!auth logs`, `b!auth setup`")

    @auth_group.command(name="channel")
    async def auth_channel(self, ctx, channel: discord.TextChannel):
        if not self.is_allowed(ctx): return
        self.get_guild_config(ctx.guild.id)["verify_channel"] = channel.id
        self._save_db("config")
        await ctx.send(f"✅ Verification channel set to {channel.mention}")

    @auth_group.command(name="role")
    async def auth_role(self, ctx, role: discord.Role):
        if not self.is_allowed(ctx): return
        self.get_guild_config(ctx.guild.id)["verify_role"] = role.id
        self._save_db("config")
        await ctx.send(f"✅ Post-verification role set to **{role.name}**")

    @auth_group.command(name="logs")
    async def auth_logs(self, ctx, channel: discord.TextChannel):
        if not self.is_allowed(ctx): return
        self.get_guild_config(ctx.guild.id)["logs_channel"] = channel.id
        self._save_db("config")
        await ctx.send(f"✅ Security backup logs set to {channel.mention}")

    @auth_group.command(name="setup")
    async def auth_setup(self, ctx):
        if not self.is_allowed(ctx): return
        cfg = self.get_guild_config(ctx.guild.id)
        if not cfg["verify_role"]:
            return await ctx.send("❌ Setup a verification role first using `b!auth role [@role]`")
        
        chan_id = cfg["verify_channel"] or ctx.channel.id
        channel = ctx.guild.get_channel(chan_id) or ctx.channel
        
        embed = discord.Embed(
            title="🛡️ Verification Required",
            description="Click the button below to verify your account and access the server channels.",
            color=0x2b2d31
        )
        view = discord.ui.View()
        # Points directly to your Render app login route
        url = f"https://badnam-1.onrender.com/login"
        view.add_item(discord.ui.Button(label="Verify Here", style=discord.ButtonStyle.link, url=url))
        
        await channel.send(embed=embed, view=view)
        await ctx.send(f"🚀 Verification gateway deployed in {channel.mention}")

    # ==========================================
    # 🧲 FEATURE 1: DISTINCT MEMBER RECOVERY
    # ==========================================
    @commands.command(name="pull")
    async def pull_members(self, ctx, amount: int = None):
        if not self.is_allowed(ctx): return
        if self.pulling_active:
            return await ctx.send("❌ A recovery pull operation is already running!")
        
        cfg = self.get_guild_config(ctx.guild.id)
        role_id = cfg["verify_role"]
        if not role_id:
            return await ctx.send("❌ Configure your verification role first via `b!auth role` so pulled members get access.")

        self.pulling_active = True
        await ctx.send(f"🔄 **Starting Member Recovery...** Scanning database for valid access keys.")

        success, failed = 0, 0
        token_list = list(self.tokens.items())
        if amount:
            token_list = token_list[:amount]

        async with aiohttp.ClientSession() as session:
            for user_id, keys in token_list:
                if not self.pulling_active: 
                    await ctx.send("🛑 Member pulling forcefully stopped.")
                    break
                
                # Check if user is already in server
                if ctx.guild.get_member(int(user_id)):
                    continue

                url = f"https://discord.com/api/v10/guilds/{ctx.guild.id}/members/{user_id}"
                headers = {
                    "Authorization": f"Bot {self.bot.http.token}",
                    "Content-Type": "application/json"
                }
                body = {"access_token": keys["access_token"]}
                
                async with session.put(url, headers=headers, json=body) as resp:
                    if resp.status in [201, 204]:
                        success += 1
                        # Force assign verified role
                        try:
                            member = ctx.guild.get_member(int(user_id))
                            if member:
                                role = ctx.guild.get_role(role_id)
                                if role: await member.add_roles(role)
                        except: pass
                    else:
                        failed += 1
                
                # Sleep to strictly respect Discord API rate limits
                await asyncio.sleep(0.8)

        self.pulling_active = False
        await ctx.send(f"🏁 **Member Recovery Finished.** Successfully pulled: `{success}` | Failed/Expired: `{failed}`")

    @commands.command(name="stoppull")
    async def stop_pull(self, ctx):
        if not self.is_allowed(ctx): return
        self.pulling_active = False
        await ctx.send("🛑 Aborting active member recovery operation immediately.")

    @commands.command(name="users")
    async def total_users(self, ctx):
        if not self.is_allowed(ctx): return
        await ctx.send(f"📊 There are currently **{len(self.tokens)}** verified member keys saved in your database backup.")

    # ==========================================
    # 📦 FEATURE 2: DISTINCT SNAPSHOT RECOVERY (CHANNELS & ROLES)
    # ==========================================
    @commands.group(name="snapshot", invoke_without_command=True)
    async def snapshot_group(self, ctx):
        if not self.is_allowed(ctx): return
        await ctx.send("⚙️ **Snapshot Options:** `b!snapshot create`, `b!snapshot channels`, `b!snapshot roles`")

    @snapshot_group.command(name="create")
    async def snapshot_create(self, ctx):
        if not self.is_allowed(ctx): return
        await ctx.send("📸 Memorizing server channels, layouts, roles, and structural permissions...")
        
        roles_data = []
        for r in ctx.guild.roles:
            if r.is_default() or r.managed: continue
            roles_data.append({
                "name": r.name,
                "color": r.color.value,
                "hoist": r.hoist,
                "mentionable": r.mentionable,
                "permissions": r.permissions.value
            })

        channels_data = []
        for c in ctx.guild.channels:
            channels_data.append({
                "name": c.name,
                "type": str(c.type),
                "category": c.category.name if c.category else None,
                "position": c.position
            })

        self.snapshots[str(ctx.guild.id)] = {
            "roles": roles_data,
            "channels": channels_data
        }
        self._save_db("snapshot")
        await ctx.send("✅ **Server Snapshot Saved!** Channels structural data and roles archived securely.")

    @snapshot_group.command(name="channels")
    async def restore_channels(self, ctx):
        if not self.is_allowed(ctx): return
        gid = str(ctx.guild.id)
        if gid not in self.snapshots or "channels" not in self.snapshots[gid]:
            return await ctx.send("❌ No structure snapshot found for this server. Use `b!snapshot create` first.")

        await ctx.send("🛠️ **Rebuilding Server Channels...** Please wait.")
        categories = {}
        
        # Re-create categories first
        for chan in sorted(self.snapshots[gid]["channels"], key=lambda x: x["position"]):
            if chan["type"] == "category":
                cat = await ctx.guild.create_category(name=chan["name"])
                categories[chan["name"]] = cat

        # Re-create Text and Voice channels
        for chan in sorted(self.snapshots[gid]["channels"], key=lambda x: x["position"]):
            cat_obj = categories.get(chan["category"]) if chan["category"] else None
            if chan["type"] == "text":
                await ctx.guild.create_text_channel(name=chan["name"], category=cat_obj)
            elif chan["type"] == "voice":
                await ctx.guild.create_voice_channel(name=chan["name"], category=cat_obj)
                
        await ctx.send("✅ All layout categories and channels fully cloned and restored.")

    @snapshot_group.command(name="roles")
    async def restore_roles(self, ctx):
        if not self.is_allowed(ctx): return
        gid = str(ctx.guild.id)
        if gid not in self.snapshots or "roles" not in self.snapshots[gid]:
            return await ctx.send("❌ No roles snapshot found for this server.")

        await ctx.send("🛡️ **Restoring Server Roles...**")
        for r_data in self.snapshots[gid]["roles"]:
            try:
                await ctx.guild.create_role(
                    name=r_data["name"],
                    color=discord.Color(r_data["color"]),
                    hoist=r_data["hoist"],
                    mentionable=r_data["mentionable"],
                    permissions=discord.Permissions(r_data["permissions"])
                )
            except: pass
        await ctx.send("✅ All server roles fully re-generated from the snapshot database.")

    # ==========================================
    # ⚡ FEATURE 3: DISTINGUISHED "RECOVER ALL"
    # ==========================================
    @commands.command(name="recoverall")
    async def recover_all(self, ctx):
        if not self.is_allowed(ctx): return
        
        confirm_embed = discord.Embed(
            title="⚠️ CRITICAL RUN: Full Server Recovery",
            description="This will execute an automated sequence:\n1️⃣ Re-generate Roles\n2️⃣ Re-build Channel Layouts\n3️⃣ Mass-pull all backup Members.\n\nType `confirm` within 15 seconds to proceed.",
            color=0xffcc00
        )
        await ctx.send(embed=confirm_embed)

        def check(m): return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == 'confirm'
        try:
            await self.bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            return await ctx.send("❌ Operation timed out. Full recovery canceled.")

        # Step 1: Restore Roles
        await ctx.invoke(self.bot.get_command('snapshot roles'))
        await asyncio.sleep(2)
        
        # Step 2: Restore Channels
        await ctx.invoke(self.bot.get_command('snapshot channels'))
        await asyncio.sleep(2)
        
        # Step 3: Pull Members
        await ctx.invoke(self.bot.get_command('pull'))

    # ==========================================
    # WHITELIST ADMINISTRATIVE CONTROLS
    # ==========================================
    @commands.group(name="wl", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def wl_group(self, ctx):
        await ctx.send("⚙️ `b!wl add [@user]` | `b!wl remove [@user]` | `b!wl list`")

    @wl_group.command(name="add")
    @commands.has_permissions(administrator=True)
    async def wl_add(self, ctx, user: discord.Member):
        cfg = self.get_guild_config(ctx.guild.id)
        if user.id not in cfg["whitelist"]:
            cfg["whitelist"].append(user.id)
            self._save_db("config")
        await ctx.send(f"✅ Whitelisted {user.mention} to use backup recovery tools.")

    @wl_group.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def wl_remove(self, ctx, user: discord.Member):
        cfg = self.get_guild_config(ctx.guild.id)
        if user.id in cfg["whitelist"]:
            cfg["whitelist"].remove(user.id)
            self._save_db("config")
        await ctx.send(f"❌ Removed {user.mention} from recovery tools whitelist.")

    @wl_group.command(name="list")
    @commands.has_permissions(administrator=True)
    async def wl_list(self, ctx):
        cfg = self.get_guild_config(ctx.guild.id)
        mentions = [f"<@{uid}>" for uid in cfg["whitelist"]]
        await ctx.send(embed=discord.Embed(title="📋 Recovery Whitelist", description="\n".join(mentions) if mentions else "Empty", color=0x2b2d31))

async def setup(bot):
    await bot.add_cog(Recovery(bot))
