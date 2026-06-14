import discord
from discord.ext import commands
import asyncio
import yt_dlp
import random
import imageio_ffmpeg
import traceback

# ==========================================
# ⚙️ EXTREME YTDL PIPELINE (ANDROID MUSIC BYPASS)
# ==========================================
yt_dlp.utils.bug_reports_message = lambda *args, **kwargs: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto', 
    'source_address': '0.0.0.0', 
    # 🚨 THE FIX: Standard YouTube search but disguised as Android Music App
    'extractor_args': {
        'youtube': ['player_client=android', 'client=android_music']
    },
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
    }
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

FILTERS = {
    "clear": "-vn",
    "bassboost": "-vn -af bass=g=15,dynaudnorm=f=200",
    "nightcore": "-vn -af asetrate=48000*1.25,atempo=1.25,dynaudnorm=f=200",
    "vaporwave": "-vn -af asetrate=48000*0.8,atempo=0.8,dynaudnorm=f=200",
    "8d": "-vn -af apulsator=hz=0.09"
}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.webpage_url = data.get('webpage_url')
        self.duration = data.get('duration', 0)
        self.thumbnail = data.get('thumbnail')
        self.requester = data.get('requester')

    @classmethod
    async def extract_info(cls, query, requester, loop=None):
        loop = loop or asyncio.get_event_loop()
        is_url = query.startswith("http")
        
        # Back to standard ytsearch so it doesn't crash the URL reader
        search_query = query if is_url else f"ytsearch:{query}"
        
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(search_query, download=False))
        except Exception as e:
            print(f"❌ YTDL EXTRACTION ERROR: {e}")
            raise e
            
        if 'entries' in data:
            if len(data['entries']) > 0:
                data = data['entries'][0]
            else:
                raise Exception("Search returned zero results. Try a direct link!")
            
        data['requester'] = requester
        return data

    @classmethod
    async def create_source(cls, data, filter_key="clear", volume=0.5):
        ff_opts = ffmpeg_options.copy()
        ff_opts['options'] = FILTERS.get(filter_key, "-vn")
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        return cls(discord.FFmpegPCMAudio(data['url'], executable=ffmpeg_path, **ff_opts), data=data, volume=volume)

class PlayerControls(discord.ui.View):
    def __init__(self, player):
        super().__init__(timeout=None)
        self.player = player

    @discord.ui.button(label="Play/Pause", emoji="⏯️", style=discord.ButtonStyle.primary, row=0)
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc:
            if vc.is_paused(): vc.resume()
            else: vc.pause()
        await interaction.response.defer()

    @discord.ui.button(label="Skip", emoji="⏭️", style=discord.ButtonStyle.secondary, row=0)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc: vc.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Loop", emoji="🔁", style=discord.ButtonStyle.secondary, row=0)
    async def loop_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.player.loop_song:
            self.player.loop_song = False
            self.player.loop_queue = True
            mode = "Queue"
        elif self.player.loop_queue:
            self.player.loop_queue = False
            mode = "Off"
        else:
            self.player.loop_song = True
            mode = "Song"
        await interaction.response.send_message(f"🔁 Loop mode set to: **{mode}**", ephemeral=True)

    @discord.ui.button(label="Shuffle", emoji="🔀", style=discord.ButtonStyle.secondary, row=1)
    async def shuffle(self, interaction: discord.Interaction, button: discord.ui.Button):
        random.shuffle(self.player.queue)
        await interaction.response.send_message("🔀 Queue shuffled!", ephemeral=True)

    @discord.ui.button(label="Stop", emoji="⏹️", style=discord.ButtonStyle.danger, row=1)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player.queue.clear()
        vc = interaction.guild.voice_client
        if vc: vc.stop()
        await interaction.response.defer()

class MusicPlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self.queue = []
        self.next = asyncio.Event()
        self.current = None
        self.volume = 0.5
        self.filter = "clear"
        self.stay_247 = False
        self.loop_queue = False
        self.loop_song = False
        self.ui_message = None
        self.player_task = self.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()
            if not self.queue and not self.stay_247:
                await asyncio.sleep(60)
                if not self.queue:
                    await self.destroy()
                    return

            if self.queue:
                if self.loop_song and self.current:
                    pass 
                else:
                    self.current = self.queue.pop(0)

                try:
                    fresh_data = await YTDLSource.extract_info(self.current['webpage_url'], self.current['requester'], self.bot.loop)
                    source = await YTDLSource.create_source(fresh_data, self.filter, self.volume)
                except Exception as e:
                    await self._channel.send(embed=discord.Embed(title="❌ Playback Error", description=f"```\n{e}\n
```", color=0xff0000))
                    continue

                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
                
                embed = discord.Embed(title="🎶 Now Playing", description=f"**[{fresh_data.get('title')}]({fresh_data.get('webpage_url')})**", color=0x2b2d31)
                embed.add_field(name="Filter", value=f"`{self.filter.title()}`", inline=True)
                embed.add_field(name="Requested By", value=f"{self.current['requester'].mention}", inline=True)
                if fresh_data.get('thumbnail'): embed.set_thumbnail(url=fresh_data['thumbnail'])
                
                if self.ui_message:
                    try: await self.ui_message.delete()
                    except: pass
                
                self.ui_message = await self._channel.send(embed=embed, view=PlayerControls(self))
                await self.next.wait()

                if self.loop_queue and not self.loop_song:
                    self.queue.append(self.current)
            else:
                await asyncio.sleep(1)

    async def destroy(self):
        if self._guild.voice_client:
            await self._guild.voice_client.disconnect()
        if self.ui_message:
            try: await self.ui_message.delete()
            except: pass
        self.bot.get_cog("Music").players.pop(self._guild.id, None)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    def get_player(self, ctx):
        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)
        return self.players[ctx.guild.id]

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("❌ You must be in a voice channel.")
        
        vc = ctx.guild.voice_client
        if not vc:
            try:
                await ctx.author.voice.channel.connect()
            except Exception as e:
                return await ctx.send(f"❌ **Error joining:** `{e}`")
        elif vc.channel != ctx.author.voice.channel:
            return await ctx.send("❌ We must be in the same channel.")

        msg = await ctx.send("🔍 **Searching...**")
        player = self.get_player(ctx)

        try:
            data = await YTDLSource.extract_info(query, ctx.author, self.bot.loop)
            player.queue.append(data)
            await msg.edit(content=None, embed=discord.Embed(description=f"✅ **Added to queue:** `{data.get('title')}`", color=0x23a55a))
        except Exception as e:
            traceback.print_exc()
            await msg.edit(content=None, embed=discord.Embed(title="❌ Search Failed", description=f"```\n{e}\n```", color=0xff0000))

    @commands.command(name="stop", aliases=["leave"])
    async def stop(self, ctx):
        if ctx.guild.id in self.players:
            player = self.players[ctx.guild.id]
            player.queue.clear()
            await player.destroy()
            await ctx.send("🛑 **Stopped.**")
        else:
            if ctx.guild.voice_client: await ctx.guild.voice_client.disconnect()

    @commands.command(name="skip", aliases=["s"])
    async def skip(self, ctx):
        vc = ctx.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("⏭️ **Skipped.**")

    @commands.command(name="queue", aliases=["q"])
    async def queue(self, ctx):
        player = self.get_player(ctx)
        if not player.queue:
            return await ctx.send("📭 **Empty queue.**")
        
        desc = ""
        for i, track in enumerate(player.queue[:10]):
            desc += f"**{i+1}.** [{track.get('title')}]({track.get('webpage_url')})\n"
        
        embed = discord.Embed(title="📜 Queue", description=desc, color=0x2b2d31)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
