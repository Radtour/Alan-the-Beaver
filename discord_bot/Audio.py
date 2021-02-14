import asyncio
import os
import random
import discord
from discord.ext import commands
from mutagen.mp3 import MP3


class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):

        if channel is None:
            channel = ctx.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(aliases=['maul', 'fresse', 'schnauze', 'halt'])
    async def stop(self, ctx):
        ctx.voice_client.stop()

    @commands.command(aliases=['raus'])
    async def quit(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, query):
        await self.join(ctx=ctx, channel=None)

        if not query.__contains__(".mp3"):
            query = query + ".mp3"

        path = find_audio_file(query)
        # print(str(path) + str(query))
        if os.path.isfile(path + query):

            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path + query))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send('Now playing: {}'.format(query))

        else:
            await ctx.send("Soundfile not found !")

    @commands.command()
    async def bye(self, ctx: discord.ext.commands.Context):
        pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles') + "!bye/")
        amount = len(pathfinder)
        sound_nr = random.randint(0, amount - 1)
        audio = MP3(os.environ.get('Discord_Bot_Soundfiles') + "!bye/" + pathfinder[sound_nr])
        length = audio.info.length
        # await ctx.send(length)
        await self.play(ctx=ctx, query=pathfinder[sound_nr])
        await asyncio.sleep(length - 1.5)
        await raus(ctx=ctx)

    @commands.command(aliases=['BIGMAC'])
    async def bigmac(self, ctx, *, member: discord.Member):
        await self.play(ctx=ctx, query="BIGMAC")
        await asyncio.sleep(1.)
        await member.move_to(None)


async def raus(ctx: discord.ext.commands.Context):
    await asyncio.sleep(1.)
    await ctx.author.move_to(None)


def find_audio_file(sound_id):
    for root, dirs, files in os.walk(os.environ.get('Discord_Bot_Soundfiles'), topdown=True):
        for file in files:
            if file.casefold() == sound_id.casefold():
                return root + "\\"
