import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
import aiohttp

# ==========================================
# 🎨 INTERACTIVE VERIFICATION UI SYSTEM
# ==========================================
class SetupModal(discord.ui.Modal, title='Customize Embed'):
    emb_title = discord.ui.TextInput(label='Title', default='BADNAM SECURITY', max_length=200)
    emb_desc = discord.ui.TextInput(label='Description', style=discord.TextStyle.paragraph, max_length=1000)
    emb_color = discord.ui.TextInput(label='Hex Color (Without #)', default='ff0000', max_length=6)
    emb_image = discord.ui.TextInput(label='Image URL (Optional)', required=False)

    def __init__(self, view, cog, guild_id):
        super().__init__()
        self.view_obj = view
        self.cog = cog
        self.guild_id = guild_id
        
        cfg = self.cog.get_guild_config(self.guild_id)
        self.emb_title.default = cfg.get("embed_title", "BADNAM SECURITY")
        self.emb_desc.default = cfg.get("embed_desc", "MUST VERIFY HERE TO ACCESS ALL CHANNELS\n(AFTER DONE NO NEED TO CLICK CONTINUE DIRECTLY COME TO THE SERVER YOU CAN ACCESS TO ALL THE CHANNELS)")
        self.emb_color.default = cfg.get("embed_color", "ff0000")
        self.emb_image.default = cfg.get("embed_image", "")

    async def on_submit(self, interaction: discord.Interaction):
        cfg = self.cog.get_guild_config(self.guild_id)
        cfg["embed_title"] = self.emb_title.value
        cfg["embed_desc"] = self.emb_desc.value
        cfg["embed_color"] = self.emb_color.value
        cfg["embed_image"] = self.emb_image.value
        self.cog._save_db("config")
        
        await self.view_obj.update_preview(interaction)

class SetupConfigView(discord.ui.View):
    def __init__(self, cog, ctx, target_channel):
        super().__init__(timeout=300)
        self.cog = cog
        self.ctx = ctx
        self.target_channel = target_channel

    async def update_preview(self, interaction):
        cfg = self.cog.get_guild_config(self.ctx.guild.id)
        
        try: color = int(cfg["embed_color"], 16)
        except: color = 0xff0000

        preview_embed = discord.Embed(title=cfg["embed_title"], description=cfg["embed_desc"], color=color)
        if cfg["embed_image"].startswith("http"):
            preview_embed.set_image(url=cfg["embed_image"])

        verify_view = discord.ui.View()
        url = f"https://badnam-1.onrender.com/login"
        verify_view.add_item(discord.ui.Button(label="Verify Here", style=discord.ButtonStyle.link, url=url, emoji="✅"))

        await interaction.response.edit_message(embeds=[preview_embed, interaction.message.embeds[1]], view=self)

    @discord.ui.button(label="Edit Embed (Title, Desc, Color, Image)", style=discord.ButtonStyle.primary, emoji="✏️", row=0)
    async def edit_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SetupModal(self, self.cog, self.ctx.guild.id))

    @discord.ui.button(label="Button Settings", style=discord.ButtonStyle.secondary, emoji="🔘", row=1)
    async def btn_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔘 Button settings locked to default OAuth link for security.", ephemeral=True)

    @discord.ui.button(label="Continue to Channels", style=discord.ButtonStyle.success, emoji="✅", row=2)
    async def confirm_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        cfg = self.cog.get_guild_config(self.ctx.guild.id)
        try: color = int(cfg["embed_color"], 16)
        except: color = 0xff0000

        final_embed = discord.Embed(title=cfg["embed_title"], description=cfg["embed_desc"], color=color)
        if cfg["embed_image"].startswith("http"):
            final_embed.set_image(url=cfg["embed_image"])

        final_view = discord.ui.View(timeout=None)
        url = f"https://badnam-1.onrender.com/login"
        final_view.add_item(discord.ui.Button(label="Verify Here", style=discord.ButtonStyle.link, url=url, emoji="✅"))

        await self.target_channel.send(embed=final_embed, view=final_view)
        await interaction.response.edit_message(content=f"✅ Setup Complete! Panel sent to {self.target_channel.mention}", embeds=[], view=None)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, emoji="❌", row=2)
    async def cancel_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Setup cancelled.", embeds=[], view=None)


# ==========================================
# ⚙️ MAIN RECOVERY COG
# ==========================================
class Recovery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "recovery_config.json"
        self.tokens_file = "oauth_tokens.json"
        self.snapshot_file = "server_snapshots.json"
        self.pulling_active = False
        self._load_dbs()
        self.auto_verify_loop.start()

    def cog_unload(self):
        self.auto_verify_loop.cancel()

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
                "embed_title": "BADNAM SECURITY",
                "embed_desc": "MUST VERIFY HERE TO ACCESS ALL CHANNELS\n(AFTER DONE NO NEED TO CLICK CONTINUE DIRECTLY COME TO THE SERVER YOU CAN ACCESS TO ALL THE CHANNELS)",
                "embed_color": "ff0000",
                "embed_image": ""
            }
        return self.config[gid]

    def is_allowed(self, ctx):
        if ctx.author.guild_permissions.administrator: return True
        return ctx.author.id in self.get_guild_config(ctx.guild.id)["whitelist"]

    # ==========================================
    # ⚡ STICKY VERIFIED ROLE (INSTANT JOIN)
    # ==========================================
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self._load_dbs()
        if str(member.id) in self.tokens:
            cfg = self.get_guild_config(member.guild.id)
            role_id = cfg.get("verify_role")
            if role_id:
                role = member.guild.get_role(role_id)
                if role:
                    try: await member.add_roles(role)
                    except: pass

    # ==========================================
    # 🔄 AUTO ROLE ASSIGNER (BACKGROUND TASK)
    # ==========================================
    @tasks.loop(seconds=5)
    async def auto_verify_loop(self):
        try:
            self._load_dbs()
            for guild_id_str, cfg in self.config.items():
                role_id = cfg.get("verify_role")
                if not role_id: continue
                guild = self.bot.get_guild(int(guild_id_str))
                if not guild: continue
                role = guild.get_role(role_id)
                if not role: continue

                for user_id in list(self.tokens.keys()):
                    member = guild.get_member(int(user_id))
                    if member and role not in member.roles:
                        try: await member.add_roles(role)
                        except: pass
        except Exception:
            pass

    @auto_verify_loop.before_loop
    async def before_auto_verify(self):
        await self.bot.wait_until_ready()

    # ==========================================
    # 🔗 VERIFICATION GATEWAY & CONFIG
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

    @auth_group.command(name="setup")
    async def auth_setup(self, ctx):
        if not self.is_allowed(ctx): return
        cfg = self.get_guild_config(ctx.guild.id)
        if not cfg["verify_role"]:
            return await ctx.send("❌ Setup a verification role first using `b!auth role [@role]`")
        
        chan_id = cfg["verify_channel"] or ctx.channel.id
        target_channel = ctx.guild.get_channel(chan_id) or ctx.channel

        try: color = int(cfg["embed_color"], 16)
        except: color = 0xff0000

        preview_embed = discord.Embed(title=cfg["embed_title"], description=cfg["embed_desc"], color=color)
        if cfg["embed_image"].startswith("http"):
            preview_embed.set_image(url=cfg["embed_image"])

        config_embed = discord.Embed(
            title="Customize Your Verification",
            description="Make this verification message truly yours!\nClick the **Edit Embed** button below to change the text and colors.",
            color=0x2b2d31
        )

        view = SetupConfigView(self, ctx, target_channel)
        await ctx.send(embeds=[preview_embed, config_embed], view=view)

    # ==========================================
    # 🧲 MEMBER RECOVERY (PULLING)
    # ==========================================
    @commands.command(name="users")
    async def total_users(self, ctx):
        if not self.is_allowed(ctx): return
        self._load_dbs() 
        await ctx.send(f"📊 There are currently **{len(self.tokens)}** verified member keys saved in your database backup.")

    @commands.command(name="pull")
    async def pull_members(self, ctx, amount: int = None):
        if not self.is_allowed(ctx): return
        if self.pulling_active:
            return await ctx.send("❌ A recovery pull operation is already running!")
        
        cfg = self.get_guild_config(ctx.guild.id)
        role_id = cfg["verify_role"]
        if not role_id:
            return await ctx.send("❌ Configure your verification role first via `b!auth role`.")

        CLIENT_ID = os.environ.get("CLIENT_ID")
        CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

        if not CLIENT_ID or not CLIENT_SECRET:
            return await ctx.send("❌ Setup Error: CLIENT_ID and CLIENT_SECRET environment variables are missing on Render.")

        self.pulling_active = True
        self._load_dbs() 
        
        msg = await ctx.send(f"🔄 **Starting Member Recovery...** Scanning database.")

        success = 0
        failed_api = 0
        failed_refresh = 0
        skipped_present = 0

        token_list = list(self.tokens.items())
        if amount: token_list = token_list[:amount]

        async with aiohttp.ClientSession() as session:
            for user_id, keys in token_list:
                if not self.pulling_active: 
                    await ctx.send("🛑 Member pulling forcefully stopped.")
                    break
                
                if ctx.guild.get_member(int(user_id)):
                    skipped_present += 1
                    continue

                url = f"https://discord.com/api/v10/guilds/{ctx.guild.id}/members/{user_id}"
                headers = {"Authorization": f"Bot {self.bot.http.token}", "Content-Type": "application/json"}
                body = {"access_token": keys["access_token"]}
                
                async with session.put(url, headers=headers, json=body) as resp:
                    if resp.status in [201, 204]:
                        success += 1
                        await asyncio.sleep(1)
                        try:
                            member = ctx.guild.get_member(int(user_id)) or await ctx.guild.fetch_member(int(user_id))
                            if member:
                                role = ctx.guild.get_role(role_id)
                                if role: await member.add_roles(role)
                        except: pass
                    else:
                        refresh_data = {
                            'client_id': CLIENT_ID,
                            'client_secret': CLIENT_SECRET,
                            'grant_type': 'refresh_token',
                            'refresh_token': keys["refresh_token"]
                        }
                        refresh_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                        
                        async with session.post("https://discord.com/api/v10/oauth2/token", data=refresh_data, headers=refresh_headers) as refresh_resp:
                            if refresh_resp.status == 200:
                                new_tokens = await refresh_resp.json()
                                self.tokens[user_id]["access_token"] = new_tokens["access_token"]
                                self.tokens[user_id]["refresh_token"] = new_tokens["refresh_token"]
                                self._save_db("tokens")

                                body = {"access_token": new_tokens["access_token"]}
                                async with session.put(url, headers=headers, json=body) as final_resp:
                                    if final_resp.status in [201, 204]: 
                                        success += 1
                                        await asyncio.sleep(1)
                                        try:
                                            member = ctx.guild.get_member(int(user_id)) or await ctx.guild.fetch_member(int(user_id))
                                            role = ctx.guild.get_role(role_id)
                                            if member and role: await member.add_roles(role)
                                        except: pass
                                    else: failed_api += 1
                            else: failed_refresh += 1
                                
                await asyncio.sleep(0.8)

        self.pulling_active = False
        
        embed = discord.Embed(title="🏁 Member Recovery Finished", color=0x2b2d31)
        embed.add_field(name="✅ Successfully Pulled", value=f"`{success}`", inline=True)
        embed.add_field(name="⏭️ Skipped (Already Here)", value=f"`{skipped_present}`", inline=True)
        embed.add_field(name="❌ Failed (Discord API)", value=f"`{failed_api}`", inline=True)
        embed.add_field(name="💀 Failed (Dead Tokens)", value=f"`{failed_refresh}`", inline=True)
        
        await msg.edit(content=None, embed=embed)

    @commands.command(name="stoppull")
    async def stop_pull(self, ctx):
        if not self.is_allowed(ctx): return
        self.pulling_active = False
        await ctx.send("🛑 Aborting active member recovery operation immediately.")

    # ==========================================
    # 📦 SERVER SNAPSHOTS (ROLES & CHANNELS)
    # ==========================================
    @commands.group(name="snapshot", invoke_without_command=True)
    async def snapshot_group(self, ctx):
        if not self.is_allowed(ctx): return
        await ctx.send("⚙️ **Snapshot Options:** `b!snapshot create`, `b!snapshot channels`, `b!snapshot roles`")

    @snapshot_group.command(name="create")
    async def snapshot_create(self, ctx):
        if not self.is_allowed(ctx): return
        await ctx.send("📸 Memorizing server channels, layouts, roles, and structural permissions...")
        
        roles_data = [{"name": r.name, "color": r.color.value, "hoist": r.hoist, "mentionable": r.mentionable, "permissions": r.permissions.value} for r in ctx.guild.roles if not r.is_default() and not r.managed]
        channels_data = [{"name": c.name, "type": str(c.type), "category": c.category.name if c.category else None, "position": c.position} for c in ctx.guild.channels]

        self.snapshots[str(ctx.guild.id)] = {"roles": roles_data, "channels": channels_data}
        self._save_db("snapshot")
        await ctx.send("✅ **Server Snapshot Saved!** Channels structural data and roles archived securely.")

    @snapshot_group.command(name="channels")
    async def restore_channels(self, ctx):
        if not self.is_allowed(ctx): return
        gid = str(ctx.guild.id)
        if gid not in self.snapshots or "channels" not in self.snapshots[gid]:
            return await ctx.send("❌ No structure snapshot found. Use `b!snapshot create` first.")

        await ctx.send("🛠️ **Rebuilding Server Channels...**")
        categories = {}
        for chan in sorted(self.snapshots[gid]["channels"], key=lambda x: x["position"]):
            if chan["type"] == "category":
                categories[chan["name"]] = await ctx.guild.create_category(name=chan["name"])

        for chan in sorted(self.snapshots[gid]["channels"], key=lambda x: x["position"]):
            cat_obj = categories.get(chan["category"])
            if chan["type"] == "text": await ctx.guild.create_text_channel(name=chan["name"], category=cat_obj)
            elif chan["type"] == "voice": await ctx.guild.create_voice_channel(name=chan["name"], category=cat_obj)
        await ctx.send("✅ All layout categories and channels fully cloned and restored.")

    @snapshot_group.command(name="roles")
    async def restore_roles(self, ctx):
        if not self.is_allowed(ctx): return
        gid = str(ctx.guild.id)
        if gid not in self.snapshots or "roles" not in self.snapshots[gid]: return await ctx.send("❌ No roles snapshot found.")

        await ctx.send("🛡️ **Restoring Server Roles...**")
        for r_data in self.snapshots[gid]["roles"]:
            try: await ctx.guild.create_role(name=r_data["name"], color=discord.Color(r_data["color"]), hoist=r_data["hoist"], mentionable=r_data["mentionable"], permissions=discord.Permissions(r_data["permissions"]))
            except: pass
        await ctx.send("✅ All server roles fully re-generated.")

    # ==========================================
    # ⚡ RECOVER ALL
    # ==========================================
    @commands.command(name="recoverall")
    async def recover_all(self, ctx):
        if not self.is_allowed(ctx): return
        await ctx.send(embed=discord.Embed(title="⚠️ CRITICAL RUN: Full Recovery", description="Type `confirm` within 15s to rebuild roles, channels, and pull members.", color=0xffcc00))
        try: await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == 'confirm', timeout=15.0)
        except asyncio.TimeoutError: return await ctx.send("❌ Timed out.")

        await ctx.invoke(self.bot.get_command('snapshot roles'))
        await asyncio.sleep(2)
        await ctx.invoke(self.bot.get_command('snapshot channels'))
        await asyncio.sleep(2)
        await ctx.invoke(self.bot.get_command('pull'))

    # ==========================================
    # 👥 WHITELIST
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
        await ctx.send(f"✅ Whitelisted {user.mention}")

    @wl_group.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def wl_remove(self, ctx, user: discord.Member):
        cfg = self.get_guild_config(ctx.guild.id)
        if user.id in cfg["whitelist"]:
            cfg["whitelist"].remove(user.id)
            self._save_db("config")
        await ctx.send(f"❌ Removed {user.mention}")

    @wl_group.command(name="list")
    @commands.has_permissions(administrator=True)
    async def wl_list(self, ctx):
        cfg = self.get_guild_config(ctx.guild.id)
        mentions = [f"<@{uid}>" for uid in cfg["whitelist"]]
        await ctx.send(embed=discord.Embed(title="📋 Recovery Whitelist", description="\n".join(mentions) if mentions else "Empty", color=0x2b2d31))

async def setup(bot):
    await bot.add_cog(Recovery(bot))
