import asyncio
from discord.ext import commands
from discord_bot.Audio import Audio
from discord_bot.YoutubePlayer import YoutubePlayer


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
    async def next(self, ctx):
        ctx.voice_client.stop()
        self.is_playing_video = False
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
