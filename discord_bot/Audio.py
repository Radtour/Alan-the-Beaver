import asyncio
import os
import random
import discord
from discord.ext import commands
from mutagen.mp3 import MP3

from discord_bot.YoutubePlayer import YoutubePlayer


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
        audio_cog = self.client.get_cog('YoutubeAudio')
        audio_cog.is_playing_video = False

    @commands.command(aliases=['raus'])
    async def quit(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, query):

        await ctx.invoke(self.client.get_command('join'))

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

    @commands.command(aliases=['soundfile', 'soundfiles'])
    async def soundlist(self, ctx, query=None):
        sound_list = "<:peepoClown:806233172564115467> SOUND-FILES <:peepoClown:806233172564115467>\n\n"

        if query is not None:

            if query.__contains__("meme"):
                query = "meme"
            elif query.__contains__("saufi"):
                query = "saufi"
            elif query.__contains__("sounds"):
                query = "sounds"
            else:
                existing_categories = search_categories()
                await ctx.send("Error: category not found.\n\nExisting categories:\n" + existing_categories)
                return

            pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles') + query)
            for i in range(len(pathfinder)):
                location = pathfinder[i].find(".mp3")
                sound_list += pathfinder[i][:location] + "\n"
            await ctx.send(sound_list)
        else:
            existing_categories = search_categories()
            await ctx.send(f"\n Categories: \n{existing_categories}")

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

    @commands.command()
    async def bigmac(self, ctx, *, member: discord.Member):
        await self.play(ctx=ctx, query="BIGMAC")
        await asyncio.sleep(1.)
        await member.move_to(None)

    @commands.command()
    async def download(self, ctx, url, name):

        if find_audio_file(name + ".mp3") is None:
            player = await YoutubePlayer.from_url(url, loop=self.client.loop)
            src_path = os.path.realpath('.') + '\\' + 'download.mp3'
            dest_path = os.environ.get('Discord_Bot_Soundfiles') + "download\\" + name + '.mp3'
            os.rename(src_path, dest_path)
            await ctx.send('Download: {}'.format(player.title))
        else:
            await ctx.send(f'Error: Sound "{name}" already existing')


async def raus(ctx: discord.ext.commands.Context):
    await asyncio.sleep(1.)
    await ctx.author.move_to(None)


def find_audio_file(sound_id):
    for root, dirs, files in os.walk(os.environ.get('Discord_Bot_Soundfiles'), topdown=True):
        for file in files:
            if file.casefold() == sound_id.casefold():
                return root + "\\"

    return None


def search_categories():
    existing_categories = ""
    pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles'))
    for i in range(len(pathfinder)):
        if not pathfinder[i].__contains__(".mp3") and not pathfinder[i] == "!bye":
            existing_categories += pathfinder[i] + "\n"

    return existing_categories
