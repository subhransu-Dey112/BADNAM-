import discord
from discord.ext import commands
import json
import os

class CustomRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "customroles_db.json"
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
            self.db[gid] = {"managers": [], "roles": []}
        return self.db[gid]

    # Security Check: Is the user an Admin or a registered Manager?
    def is_manager(self, ctx):
        if ctx.author.guild_permissions.administrator: return True
        data = self.get_data(ctx.guild.id)
        for m in data["managers"]:
            if ctx.author.id == m or any(r.id == m for r in ctx.author.roles):
                return True
        return False

    # ==========================================
    # CUSTOM ROLE COMMANDS
    # ==========================================
    @commands.group(name="setup", aliases=["customrole", "cr"], invoke_without_command=True)
    async def setup_base(self, ctx):
        await ctx.send("Use `b!setup create`, `delete`, `add`, `remove`, `set manager`, `list`, `config`, `reset`.")

    @setup_base.command(name="help")
    async def setup_help(self, ctx):
        await ctx.invoke(self.setup_base)

    # --- CREATE & DELETE ---
    @setup_base.command(name="create")
    async def setup_create(self, ctx, member: discord.Member, hex_color: str, *, name: str):
        if not self.is_manager(ctx): return await ctx.send("❌ You do not have permission to manage Custom Roles.")
        
        try:
            color = discord.Color(int(hex_color.replace("#", ""), 16))
        except ValueError:
            return await ctx.send("❌ Invalid color! Please use a hex code like `#FF5733`.")

        try:
            role = await ctx.guild.create_role(name=name, color=color, reason=f"Custom Role created by {ctx.author}")
            await member.add_roles(role)
            
            data = self.get_data(ctx.guild.id)
            data["roles"].append(role.id)
            self._save_db()
            
            await ctx.send(f"✅ Successfully created **{role.name}** and assigned it to {member.mention}.")
        except discord.Forbidden:
            await ctx.send("❌ I lack permissions. Ensure my bot role is higher than the roles I am creating.")

    @setup_base.command(name="delete")
    async def setup_delete(self, ctx, role: discord.Role):
        if not self.is_manager(ctx): return await ctx.send("❌ You do not have permission to manage Custom Roles.")
        
        data = self.get_data(ctx.guild.id)
        if role.id in data["roles"]:
            data["roles"].remove(role.id)
            self._save_db()
            
        try:
            await role.delete(reason=f"Custom Role deleted by {ctx.author}")
            await ctx.send(f"✅ Successfully deleted the custom role.")
        except discord.Forbidden:
            await ctx.send("❌ I lack permissions to delete that role. Ensure it is below my highest role.")

    # --- ADD & REMOVE (Assigning to users) ---
    @setup_base.command(name="add")
    async def setup_add(self, ctx, member: discord.Member, role: discord.Role):
        if not self.is_manager(ctx): return await ctx.send("❌ You do not have permission to manage Custom Roles.")
        
        data = self.get_data(ctx.guild.id)
        if role.id not in data["roles"]:
            return await ctx.send("❌ That is not a registered Custom Role.")
            
        await member.add_roles(role)
        await ctx.send(f"✅ Added {role.name} to {member.mention}.")

    @setup_base.command(name="remove")
    async def setup_remove(self, ctx, member: discord.Member, role: discord.Role):
        if not self.is_manager(ctx): return await ctx.send("❌ You do not have permission to manage Custom Roles.")
        
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"❌ Removed {role.name} from {member.mention}.")
        else:
            await ctx.send("❌ That user does not have that role.")

    # --- SET MANAGER ---
    @setup_base.group(name="set", invoke_without_command=True)
    async def setup_set(self, ctx):
        pass

    @setup_set.command(name="manager")
    @commands.has_permissions(administrator=True) # Only full Admins can assign Managers
    async def setup_set_manager(self, ctx, target: discord.Role | discord.Member):
        data = self.get_data(ctx.guild.id)
        if target.id not in data["managers"]:
            data["managers"].append(target.id)
            self._save_db()
        await ctx.send(f"👑 {target.mention} is now authorized as a Custom Role Manager.")

    # --- LIST, CONFIG & RESET ---
    @setup_base.command(name="list")
    async def setup_list(self, ctx):
        data = self.get_data(ctx.guild.id)
        roles = [f"<@&{r}>" for r in data["roles"] if ctx.guild.get_role(r)]
        if not roles: return await ctx.send("📋 No Custom Roles have been created yet.")
        await ctx.send(embed=discord.Embed(title="🎨 Active Custom Roles", description="\n".join(roles), color=0x2b2d31))

    @setup_base.command(name="config")
    async def setup_config(self, ctx):
        data = self.get_data(ctx.guild.id)
        managers = [f"<@&{m}>" if ctx.guild.get_role(m) else f"<@{m}>" for m in data["managers"]]
        
        embed = discord.Embed(title="⚙️ Custom Role Setup Config", color=0x2b2d31)
        embed.add_field(name="👑 Authorized Managers", value="\n".join(managers) if managers else "Server Admins Only", inline=False)
        embed.add_field(name="🎨 Registered Roles", value=f"{len(data['roles'])} total custom roles managed by the bot.", inline=False)
        await ctx.send(embed=embed)

    @setup_base.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def setup_reset(self, ctx):
        self.get_data(ctx.guild.id)["roles"] = []
        self.get_data(ctx.guild.id)["managers"] = []
        self._save_db()
        await ctx.send("✅ The Custom Role database has been completely wiped and reset.")

async def setup(bot):
    await bot.add_cog(CustomRoles(bot))
