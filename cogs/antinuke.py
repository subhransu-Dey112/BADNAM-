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

    # --- ANTINUKE TOGGLE ---
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

    # --- LOGS ---
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
        if data["log_channel"]:
            await ctx.send(f"📡 Current log channel: <#{data['log_channel']}>")
        else:
            await ctx.send("❌ No log channel set.")

    @antinukelog.command(name="msg")
    @commands.has_permissions(administrator=True)
    async def log_msg(self, ctx, *, message: str):
        data = self.get_data(ctx.guild.id)
        data["log_msg"] = message
        self._save_db()
        await ctx.send(f"✅ Log message updated to: `{message}`")

    # --- WHITELIST ---
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, member: discord.Member = None):
        # Adding support to just type b!whitelist @user
        if member:
            data = self.get_data(ctx.guild.id)
            if member.id not in data["whitelist"]:
                data["whitelist"].append(member.id)
                self._save_db()
                await ctx.send(f"✅ **{member.name}** is whitelisted.")
        else:
            await ctx.send("Use `b!whitelist @user`, `remove`, `show`, or `resetall`")

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

    # --- EXTRA OWNER ---
    @commands.group(invoke_without_command=True)
    async def extraowner(self, ctx):
        pass

    @extraowner.command(name="set")
    async def eo_set(self, ctx, member: discord.Member):
        if ctx.author.id != ctx.guild.owner_id: return await ctx.send("❌ Only the actual Server Owner can use this.")
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
        await ctx.send("✅ Extra Owners completely reset.")

async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
