import discord
from discord.ext import commands
import json
import os

class Automation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "autorole_db.json"
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
            self.db[gid] = {"humans": [], "bots": []}
        return self.db[gid]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = self.get_data(member.guild.id)
        role_ids = data["bots"] if member.bot else data["humans"]
        if not role_ids: return

        roles_to_add = [member.guild.get_role(r_id) for r_id in role_ids if member.guild.get_role(r_id)]
        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add, reason="AutoRole System")
            except discord.Forbidden:
                pass 

    # ==========================================
    # AUTOROLE COMMANDS
    # ==========================================
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx):
        await ctx.send("Use `b!autorole config`, `humans`, `bots`, or `reset`")

    @autorole.command(name="config", aliases=["list"])
    @commands.has_permissions(administrator=True)
    async def ar_config(self, ctx):
        data = self.get_data(ctx.guild.id)
        h_roles = [f"<@&{r}>" for r in data["humans"]]
        b_roles = [f"<@&{r}>" for r in data["bots"]]
        embed = discord.Embed(title="⚙️ AutoRole Config", color=0x2b2d31)
        embed.add_field(name="🧑 Humans", value="\n".join(h_roles) if h_roles else "None", inline=False)
        embed.add_field(name="🤖 Bots", value="\n".join(b_roles) if b_roles else "None", inline=False)
        await ctx.send(embed=embed)

    # --- HUMANS ---
    @autorole.group(name="humans", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def ar_humans(self, ctx):
        data = self.get_data(ctx.guild.id)
        h_roles = [f"<@&{r}>" for r in data["humans"]]
        await ctx.send(embed=discord.Embed(title="🧑 Human AutoRoles", description="\n".join(h_roles) if h_roles else "None set.", color=0x2b2d31))

    @ar_humans.command(name="add")
    @commands.has_permissions(administrator=True)
    async def ar_humans_add(self, ctx, role: discord.Role):
        data = self.get_data(ctx.guild.id)
        if role.id not in data["humans"]: data["humans"].append(role.id)
        self._save_db()
        await ctx.send(f"✅ Added {role.mention} to Human AutoRoles.")

    @ar_humans.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def ar_humans_remove(self, ctx, role: discord.Role):
        data = self.get_data(ctx.guild.id)
        if role.id in data["humans"]: data["humans"].remove(role.id)
        self._save_db()
        await ctx.send(f"❌ Removed {role.name} from Human AutoRoles.")

    # --- BOTS ---
    @autorole.group(name="bots", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def ar_bots(self, ctx):
        data = self.get_data(ctx.guild.id)
        b_roles = [f"<@&{r}>" for r in data["bots"]]
        await ctx.send(embed=discord.Embed(title="🤖 Bot AutoRoles", description="\n".join(b_roles) if b_roles else "None set.", color=0x2b2d31))

    @ar_bots.command(name="add")
    @commands.has_permissions(administrator=True)
    async def ar_bots_add(self, ctx, role: discord.Role):
        data = self.get_data(ctx.guild.id)
        if role.id not in data["bots"]: data["bots"].append(role.id)
        self._save_db()
        await ctx.send(f"✅ Added {role.mention} to Bot AutoRoles.")

    @ar_bots.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def ar_bots_remove(self, ctx, role: discord.Role):
        data = self.get_data(ctx.guild.id)
        if role.id in data["bots"]: data["bots"].remove(role.id)
        self._save_db()
        await ctx.send(f"❌ Removed {role.name} from Bot AutoRoles.")

    # --- RESET ---
    @autorole.group(name="reset", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def ar_reset(self, ctx):
        await ctx.send("Use `b!autorole reset humans`, `bots`, or `all`")

    @ar_reset.command(name="humans")
    @commands.has_permissions(administrator=True)
    async def ar_reset_humans(self, ctx):
        self.get_data(ctx.guild.id)["humans"] = []
        self._save_db()
        await ctx.send("✅ Human AutoRoles cleared.")

    @ar_reset.command(name="bots")
    @commands.has_permissions(administrator=True)
    async def ar_reset_bots(self, ctx):
        self.get_data(ctx.guild.id)["bots"] = []
        self._save_db()
        await ctx.send("✅ Bot AutoRoles cleared.")

    @ar_reset.command(name="all")
    @commands.has_permissions(administrator=True)
    async def ar_reset_all(self, ctx):
        data = self.get_data(ctx.guild.id)
        data["humans"], data["bots"] = [], []
        self._save_db()
        await ctx.send("✅ All AutoRoles completely wiped.")

async def setup(bot):
    await bot.add_cog(Automation(bot))
