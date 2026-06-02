import discord
from discord.ext import commands
import json
import os
import re
from collections import defaultdict
import time

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "automod_db.json"
        self._load_db()
        self.spam_cache = defaultdict(lambda: defaultdict(list))

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
                "enabled": False, "punishment": "timeout", "log_channel": None,
                "whitelist_roles": [], "whitelist_channels": [],
                "toggles": { "antispam": False, "duplicate": False, "emoji": False, "word": False, "mention": False, "link": False, "invite": False },
                "antibot": False, "antibot_wl": []
            }
        return self.db[gid]

    async def apply_punishment(self, message, reason):
        data = self.get_data(message.guild.id)
        try: await message.delete()
        except: pass
        try:
            if data["punishment"] == "timeout":
                import datetime
                await message.author.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=10), reason=reason)
                await message.channel.send(f"⏱️ **{message.author.name}** was timed out. Reason: {reason}", delete_after=5)
            elif data["punishment"] == "kick":
                await message.author.kick(reason=reason)
            elif data["punishment"] == "ban":
                await message.author.ban(reason=reason)
        except: pass
        if data["log_channel"]:
            log_chan = message.guild.get_channel(data["log_channel"])
            if log_chan: await log_chan.send(f"🛡️ **AutoMod** | User: {message.author.mention} | Action: {data['punishment']} | Reason: {reason}")

    def is_whitelisted(self, message):
        data = self.get_data(message.guild.id)
        if message.author.id == message.guild.owner_id or message.author.id == self.bot.user.id: return True
        if message.channel.id in data["whitelist_channels"]: return True
        for role in message.author.roles:
            if role.id in data["whitelist_roles"]: return True
        return False

    # ==========================================
    # AUTOMOD CORE
    # ==========================================
    @commands.group(invoke_without_command=True, aliases=["automod help"])
    @commands.has_permissions(administrator=True)
    async def automod(self, ctx):
        await ctx.send("AutoMod system. Use `b!automod enable`, `disable`, `config`, `reset`, `punishment`, `log`, `ignore`, `manage`.")

    @automod.command(name="enable")
    @commands.has_permissions(administrator=True)
    async def am_enable(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["enabled"] = True
        self._save_db()
        await ctx.send("✅ AutoMod ENABLED.")

    @automod.command(name="disable")
    @commands.has_permissions(administrator=True)
    async def am_disable(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["enabled"] = False
        self._save_db()
        await ctx.send("❌ AutoMod DISABLED.")

    @automod.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def am_reset(self, ctx):
        self.db[str(ctx.guild.id)] = self.get_data(0) # reset to default structure
        self._save_db()
        await ctx.send("✅ AutoMod completely reset to defaults.")

    @automod.command(name="config")
    @commands.has_permissions(administrator=True)
    async def am_config(self, ctx):
        data = self.get_data(ctx.guild.id)
        toggles = "\n".join([f"{k}: {'✅' if v else '❌'}" for k, v in data["toggles"].items()])
        embed = discord.Embed(title="⚙️ AutoMod Config", description=f"**Status:** {data['enabled']}\n**Punishment:** {data['punishment']}\n\n**Modules:**\n{toggles}", color=0x2b2d31)
        await ctx.send(embed=embed)

    # --- PUNISHMENTS ---
    @automod.group(name="punishment", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def am_punishment(self, ctx): pass

    @am_punishment.command(name="set")
    @commands.has_permissions(administrator=True)
    async def am_pun_set(self, ctx, p_type: str):
        if p_type.lower() not in ["timeout", "kick", "ban"]: return await ctx.send("❌ Must be timeout, kick, or ban.")
        self.get_data(ctx.guild.id)["punishment"] = p_type.lower()
        self._save_db()
        await ctx.send(f"✅ Punishment set to: **{p_type.lower()}**")

    @am_punishment.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def am_pun_reset(self, ctx):
        self.get_data(ctx.guild.id)["punishment"] = "timeout"
        self._save_db()
        await ctx.send("✅ Punishment reset to default (timeout).")

    @am_punishment.command(name="show")
    @commands.has_permissions(administrator=True)
    async def am_pun_show(self, ctx):
        await ctx.send(f"⚖️ Current punishment is: **{self.get_data(ctx.guild.id)['punishment']}**")

    # --- LOGGING ---
    @automod.group(name="log", aliases=["logging"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def am_log(self, ctx): pass

    @am_log.command(name="set")
    @commands.has_permissions(administrator=True)
    async def am_log_set(self, ctx, channel: discord.TextChannel):
        self.get_data(ctx.guild.id)["log_channel"] = channel.id
        self._save_db()
        await ctx.send(f"✅ Logs set to {channel.mention}")

    @am_log.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def am_log_reset(self, ctx):
        self.get_data(ctx.guild.id)["log_channel"] = None
        self._save_db()
        await ctx.send("✅ Logs disabled.")

    @am_log.command(name="show")
    @commands.has_permissions(administrator=True)
    async def am_log_show(self, ctx):
        ch = self.get_data(ctx.guild.id)["log_channel"]
        await ctx.send(f"📡 Log channel: <#{ch}>" if ch else "❌ No log channel set.")

    # --- WHITELISTS (IGNORE) ---
    @automod.group(name="ignore", aliases=["whitelist"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def am_wl(self, ctx): pass

    @am_wl.command(name="add")
    @commands.has_permissions(administrator=True)
    async def am_wl_add(self, ctx, target: discord.Role | discord.TextChannel):
        data = self.get_data(ctx.guild.id)
        if isinstance(target, discord.Role) and target.id not in data["whitelist_roles"]: data["whitelist_roles"].append(target.id)
        elif isinstance(target, discord.TextChannel) and target.id not in data["whitelist_channels"]: data["whitelist_channels"].append(target.id)
        self._save_db()
        await ctx.send(f"✅ Whitelisted {target.mention}")

    @am_wl.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def am_wl_remove(self, ctx, target: discord.Role | discord.TextChannel):
        data = self.get_data(ctx.guild.id)
        if isinstance(target, discord.Role) and target.id in data["whitelist_roles"]: data["whitelist_roles"].remove(target.id)
        elif isinstance(target, discord.TextChannel) and target.id in data["whitelist_channels"]: data["whitelist_channels"].remove(target.id)
        self._save_db()
        await ctx.send(f"❌ Removed {target.mention} from whitelist.")

    @am_wl.command(name="channel")
    @commands.has_permissions(administrator=True)
    async def am_wl_channel(self, ctx, channel: discord.TextChannel):
        await ctx.invoke(self.am_wl_add, channel)

    @am_wl.command(name="role")
    @commands.has_permissions(administrator=True)
    async def am_wl_role(self, ctx, role: discord.Role):
        await ctx.invoke(self.am_wl_add, role)

    @am_wl.command(name="show", aliases=["config"])
    @commands.has_permissions(administrator=True)
    async def am_wl_show(self, ctx):
        data = self.get_data(ctx.guild.id)
        roles = [f"<@&{r}>" for r in data["whitelist_roles"]]
        chans = [f"<#{c}>" for c in data["whitelist_channels"]]
        embed = discord.Embed(title="🛡️ AutoMod Whitelists", color=0x2b2d31)
        embed.add_field(name="Roles", value="\n".join(roles) if roles else "None", inline=False)
        embed.add_field(name="Channels", value="\n".join(chans) if chans else "None", inline=False)
        await ctx.send(embed=embed)

    @am_wl.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def am_wl_reset(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["whitelist_roles"], data["whitelist_channels"] = [], []
        self._save_db()
        await ctx.send("✅ Whitelists reset.")

    @automod.group(name="unignore", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def am_unignore(self, ctx): pass

    @am_unignore.command(name="channel")
    @commands.has_permissions(administrator=True)
    async def am_un_chan(self, ctx, channel: discord.TextChannel):
        await ctx.invoke(self.am_wl_remove, channel)

    @am_unignore.command(name="role")
    @commands.has_permissions(administrator=True)
    async def am_un_role(self, ctx, role: discord.Role):
        await ctx.invoke(self.am_wl_remove, role)

    # --- MANAGE TRIGGERS ---
    @automod.command(name="manage")
    @commands.has_permissions(administrator=True)
    async def am_manage(self, ctx, module: str):
        module = module.lower()
        if module not in self.get_data(ctx.guild.id)["toggles"]: return await ctx.send("❌ Choose: antispam, duplicate, emoji, word, mention, link, invite")
        self.get_data(ctx.guild.id)["toggles"][module] = not self.get_data(ctx.guild.id)["toggles"][module]
        self._save_db()
        await ctx.send(f"✅ **{module}** is now **{'ENABLED' if self.get_data(ctx.guild.id)['toggles'][module] else 'DISABLED'}**")

    # ==========================================
    # ANTIBOT SYSTEM
    # ==========================================
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antibot(self, ctx): pass

    @antibot.command(name="add")
    @commands.has_permissions(administrator=True)
    async def ab_add(self, ctx):
        self.get_data(ctx.guild.id)["antibot"] = True
        self._save_db()
        await ctx.send("✅ AntiBot ENABLED.")

    @antibot.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def ab_remove(self, ctx):
        self.get_data(ctx.guild.id)["antibot"] = False
        self._save_db()
        await ctx.send("❌ AntiBot DISABLED.")

    @antibot.command(name="wl")
    @commands.has_permissions(administrator=True)
    async def ab_wl(self, ctx, bot_id: int):
        data = self.get_data(ctx.guild.id)
        if bot_id not in data["antibot_wl"]: data["antibot_wl"].append(bot_id)
        self._save_db()
        await ctx.send(f"✅ Bot ID `{bot_id}` whitelisted.")

    @antibot.command(name="config")
    @commands.has_permissions(administrator=True)
    async def ab_config(self, ctx):
        data = self.get_data(ctx.guild.id)
        await ctx.send(f"🤖 **AntiBot:** {data['antibot']}\n📋 **Whitelisted IDs:** {len(data['antibot_wl'])}")

    @antibot.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def ab_reset(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["antibot"], data["antibot_wl"] = False, []
        self._save_db()
        await ctx.send("✅ AntiBot reset.")

    # ==========================================
    # LISTENERS
    # ==========================================
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot: return
        data = self.get_data(message.guild.id)
        if not data["enabled"] or self.is_whitelisted(message): return

        content = message.content.lower()
        if data["toggles"]["antiinvite"] and ("discord.gg/" in content or "discord.com/invite/" in content):
            return await self.apply_punishment(message, "Sending Invites")
        if data["toggles"]["antilink"] and re.search(r"http[s]?://", content):
            return await self.apply_punishment(message, "Sending Links")
        if data["toggles"]["antispam"]:
            now = time.time()
            user_cache = self.spam_cache[message.guild.id][message.author.id]
            user_cache.append(now)
            self.spam_cache[message.guild.id][message.author.id] = [t for t in user_cache if now - t <= 5.0]
            if len(self.spam_cache[message.guild.id][message.author.id]) >= 5:
                self.spam_cache[message.guild.id][message.author.id] = []
                await self.apply_punishment(message, "Spamming")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot: return
        data = self.get_data(member.guild.id)
        if data["antibot"] and member.id not in data["antibot_wl"]:
            try: await member.ban(reason="AntiBot: Unauthorized Bot")
            except: pass

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
