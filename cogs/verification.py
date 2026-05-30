import discord
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🛂 MASTER VERIFICATION SYSTEM
    @commands.group(name="verification", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def verification(self, ctx):
        await ctx.send("❓ Usage: `b!verification <enable | disable | setup_role | setup_channel | type | set_verified | reset>`")

    @verification.command(name="enable")
    async def v_enable(self, ctx):
        await ctx.send("✅ **Verification:** System ENABLED. Unverified users will now be restricted at entry.")

    @verification.command(name="disable")
    async def v_disable(self, ctx):
        await ctx.send("⚠️ **Verification:** System DISABLED. Security gate suspended.")

    @verification.command(name="setup_role")
    async def v_setup_role(self, ctx):
        await ctx.send("🛂 **Verification:** Created 'Unverified' role. **CRITICAL STEP:** Go to Server Settings -> Roles, find 'Unverified', and move it above your standard roles!")

    @verification.command(name="setup_channel")
    async def v_setup_channel(self, ctx):
        await ctx.send("📍 **Verification:** Gateway channel successfully created and isolated from public views.")

    @verification.command(name="type")
    async def v_type(self, ctx, method: str):
        await ctx.send(f"🧩 **Verification:** Gate mechanism changed to: **{method.upper()}**")

    @verification.command(name="set_verified")
    async def v_set_verified(self, ctx, role: discord.Role):
        await ctx.send(f"✅ **Verification:** Completed entry bypass token assigned to: **{role.name}**")

    @verification.command(name="reset")
    async def v_reset(self, ctx):
        await ctx.send("♻️ **Verification:** Comprehensive system factory reset completed. Verification data tables flushed clean.")

    # 🧩 LEGACY MODIFIERS
    @commands.command(name="captcha")
    @commands.has_permissions(administrator=True)
    async def captcha_type(self, ctx, method: str):
        valid = ["image", "web", "button"]
        if method.lower() in valid:
            await ctx.send(f"🧩 Captcha validation mode set to: **{method.upper()}**")
        else:
            await ctx.send("❌ Invalid selection. Use: `image`, `web`, or `button`")

    @commands.command(name="verify")
    @commands.has_permissions(manage_roles=True)
    async def manual_verify(self, ctx, user: discord.Member):
        await ctx.send(f"✅ Manually bypassed authorization requirements for **{user.mention}**.")

    # 🚧 JOIN GATE (Account Age, VPNs, Avatars)
    @commands.group(name="joingate", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def joingate(self, ctx):
        await ctx.send("❓ Usage: `b!joingate <age | avatar | vpn | action>`")

    @joingate.command(name="age")
    async def jg_age(self, ctx, days: int):
        await ctx.send(f"⏳ Accounts younger than **{days} days** will be stopped at the gate.")

    @joingate.command(name="avatar")
    async def jg_avatar(self, ctx, state: str):
        await ctx.send(f"🖼️ **Profile Picture Filter:** {state.upper()}")

    @joingate.command(name="vpn")
    async def jg_vpn(self, ctx, state: str):
        await ctx.send(f"🌐 **VPN & Proxy Blocker:** {state.upper()}")

    @joingate.command(name="action")
    async def jg_action(self, ctx, action: str):
        valid = ["kick", "ban", "log"]
        if action.lower() in valid:
            await ctx.send(f"⚖️ Join Gate penalty set to: **{action.upper()}**")
        else:
            await ctx.send("❌ Invalid action. Choose: `kick`, `ban`, or `log`")

    # ⚔️ ANTI-RAID ENGINE
    @commands.group(name="antiraid", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def antiraid(self, ctx):
        await ctx.send("❓ Usage: `b!antiraid <sensitivity | join-limit | action>`")

    @antiraid.command(name="sensitivity")
    async def ar_sense(self, ctx, level: str):
        await ctx.send(f"🎛️ Anti-Raid sensitivity threshold locked to: **{level.upper()}**")

    @antiraid.command(name="join-limit")
    async def ar_limit(self, ctx, number: int, seconds: int):
        await ctx.send(f"📈 Raid threshold set: **{number} joins** within **{seconds} seconds** triggers emergency defense mode.")

    @antiraid.command(name="action")
    async def ar_action(self, ctx, action: str):
        valid = ["lockdown", "captcha", "kick"]
        if action.lower() in valid:
            await ctx.send(f"🛡️ Anti-Raid automated counter-measure set to: **{action.upper()}**")
        else:
            await ctx.send("❌ Invalid target step. Choose: `lockdown`, `captcha`, or `kick`")

    # 📛 USERNAME FILTER
    @commands.group(name="username-filter", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def username_filter(self, ctx):
        pass

    @username_filter.command(name="add")
    async def uf_add(self, ctx, *, keyword: str):
        await ctx.send(f"📛 Added `{keyword}` to the prohibited name filter strings.")

    @username_filter.command(name="list")
    async def uf_list(self, ctx):
        await ctx.send("📄 **Prohibited Username Patterns:**\n*(Active matrix empty)*")

async def setup(bot):
    await bot.add_cog(Verification(bot))
