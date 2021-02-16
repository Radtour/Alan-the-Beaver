import asyncio

import discord

import youtube_dl
from discord.ext import commands

from discord_bot.Audio import Audio

ffmpeg_options = {
    'options': '-vn'
}

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
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YoutubePlayer(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class YoutubeAudio(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.last_url = None
        self.is_playing_video = False

    @commands.command()
    async def yt(self, ctx, *, url):
        audio_cog = self.client.get_cog('Audio')

        await Audio.join(audio_cog, ctx=ctx)
        is_playing = ctx.voice_client.is_playing()
        if not is_playing and not self.is_playing_video:
            self.is_playing_video = True
            async with ctx.typing():
                player = await YoutubePlayer.from_url(url, loop=self.client.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send('YouTube-Video: {}'.format(player.title))
            await asyncio.sleep(player.data['duration'])
            self.is_playing_video = False
        elif self.is_playing_video:
            await ctx.send('Already playing a YouTube-Video. Type "!yes" if you want to add the video to the queue.')
            self.last_url = url

        if len(self.queue) > 0:
            next_url = self.queue.pop()
            await self.yt(ctx=ctx, url=next_url)

    @commands.command()
    async def yes(self, ctx):
        self.queue.append(self.last_url)

    @commands.command()
    async def queue(self, ctx):
        queue_message = ""

        for element in self.queue:
            queue_message += element + "\n"
        await ctx.send(queue_message)







