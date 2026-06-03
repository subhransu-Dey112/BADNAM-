import discord
from discord.ext import commands
import json
import os
import asyncio

class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "interactions_db.json"
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
            self.db[gid] = {"ar": {}, "react": {}}
        return self.db[gid]

    # ==========================================
    # 💬 AUTO-RESPONDER (Aliases: att, autoresponder)
    # ==========================================
    @commands.group(invoke_without_command=True, aliases=["autoresponder", "ar"])
    @commands.has_permissions(administrator=True)
    async def att(self, ctx):
        await ctx.send("Use `b!att add trigger | reply`, `edit`, `remove`, `list`, `autodel`, or `reset`.")

    @att.command(name="add", aliases=["create"])
    @commands.has_permissions(administrator=True)
    async def att_add(self, ctx, *, args: str):
        if "|" not in args: return await ctx.send("❌ Format: `b!att add trigger | reply`")
        trigger, reply = [x.strip() for x in args.split("|", 1)]
        data = self.get_data(ctx.guild.id)
        data["ar"][trigger.lower()] = {"reply": reply, "autodel": None}
        self._save_db()
        await ctx.send(f"✅ Added autoresponder for: **{trigger}**")

    @att.command(name="edit")
    @commands.has_permissions(administrator=True)
    async def att_edit(self, ctx, *, args: str):
        if "|" not in args: return await ctx.send("❌ Format: `b!att edit trigger | new reply`")
        trigger, reply = [x.strip() for x in args.split("|", 1)]
        data = self.get_data(ctx.guild.id)
        if trigger.lower() not in data["ar"]: return await ctx.send("❌ Trigger not found.")
        data["ar"][trigger.lower()]["reply"] = reply
        self._save_db()
        await ctx.send(f"✅ Edited autoresponder for: **{trigger}**")

    @att.command(name="remove", aliases=["delete"])
    @commands.has_permissions(administrator=True)
    async def att_remove(self, ctx, *, trigger: str):
        data = self.get_data(ctx.guild.id)
        if trigger.lower() in data["ar"]:
            del data["ar"][trigger.lower()]
            self._save_db()
            await ctx.send(f"❌ Removed autoresponder for: **{trigger}**")
        else: await ctx.send("❌ Trigger not found.")

    @att.command(name="autodel")
    @commands.has_permissions(administrator=True)
    async def att_autodel(self, ctx, trigger: str, seconds: int):
        if not (1 <= seconds <= 1000): return await ctx.send("❌ Seconds must be between 1 and 1000.")
        data = self.get_data(ctx.guild.id)
        if trigger.lower() not in data["ar"]: return await ctx.send("❌ Trigger not found.")
        data["ar"][trigger.lower()]["autodel"] = seconds
        self._save_db()
        await ctx.send(f"✅ Autoresponder for **{trigger}** will auto-delete after {seconds} seconds.")

    @att.command(name="list", aliases=["config"])
    @commands.has_permissions(administrator=True)
    async def att_list(self, ctx):
        data = self.get_data(ctx.guild.id)
        ar_list = data["ar"]
        if not ar_list: return await ctx.send("📋 No autoresponders set.")
        desc = "\n".join([f"**{t}** ➔ {d['reply']} *(Delete: {d['autodel']}s)*" for t, d in ar_list.items()])
        await ctx.send(embed=discord.Embed(title="💬 AutoResponders", description=desc, color=0x2b2d31))

    @att.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def att_reset(self, ctx):
        self.get_data(ctx.guild.id)["ar"] = {}
        self._save_db()
        await ctx.send("✅ All autoresponders cleared.")

    # ==========================================
    # ✨ AUTO-REACT (Aliases: autoreact)
    # ==========================================
    @commands.group(invoke_without_command=True, aliases=["autoreact"])
    @commands.has_permissions(administrator=True)
    async def react(self, ctx):
        await ctx.send("Use `b!react add trigger | emoji`, `remove`, `list`, or `reset`.")

    @react.command(name="add")
    @commands.has_permissions(administrator=True)
    async def react_add(self, ctx, *, args: str):
        if "|" not in args: return await ctx.send("❌ Format: `b!react add trigger | emoji`")
        trigger, emoji = [x.strip() for x in args.split("|", 1)]
        data = self.get_data(ctx.guild.id)
        data["react"][trigger.lower()] = emoji
        self._save_db()
        await ctx.send(f"✅ Added autoreact {emoji} for: **{trigger}**")

    @react.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def react_remove(self, ctx, *, trigger: str):
        data = self.get_data(ctx.guild.id)
        if trigger.lower() in data["react"]:
            del data["react"][trigger.lower()]
            self._save_db()
            await ctx.send(f"❌ Removed autoreact for: **{trigger}**")
        else: await ctx.send("❌ Trigger not found.")

    @react.command(name="list")
    @commands.has_permissions(administrator=True)
    async def react_list(self, ctx):
        data = self.get_data(ctx.guild.id)
        react_list = data["react"]
        if not react_list: return await ctx.send("📋 No autoreacts set.")
        desc = "\n".join([f"**{t}** ➔ {e}" for t, e in react_list.items()])
        await ctx.send(embed=discord.Embed(title="✨ AutoReacts", description=desc, color=0x2b2d31))

    @react.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def react_reset(self, ctx):
        self.get_data(ctx.guild.id)["react"] = {}
        self._save_db()
        await ctx.send("✅ All autoreacts cleared.")

    # ==========================================
    # 👂 THE LISTENER
    # ==========================================
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot: return
        
        data = self.get_data(message.guild.id)
        content = message.content.lower()

        # Check Auto-Respond
        for trigger, info in data["ar"].items():
            if trigger in content:
                msg = await message.channel.send(info["reply"])
                if info["autodel"]:
                    await asyncio.sleep(info["autodel"])
                    try: await msg.delete()
                    except: pass
                break # Only fire one responder per message

        # Check Auto-React
        for trigger, emoji in data["react"].items():
            if trigger in content:
                try: await message.add_reaction(emoji)
                except: pass

async def setup(bot):
    await bot.add_cog(Interactions(bot))
