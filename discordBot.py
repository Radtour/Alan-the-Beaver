import asyncio
import discord
import os
import youtube_dl
import random
from discord.ext import commands
from mutagen.mp3 import MP3


intents = discord.Intents.default()
intents.voice_states = True
client = commands.Bot(command_prefix="!", help_command=None, intents=intents)

emoji_list = ["<:peepoClown:806233172564115467>"]

temporary_whitelist_labels = emoji_list + ["Existing categories", "Categories"]

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    activity = discord.Activity(name="hunting with a cleaver", type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.command()
async def test(ctx):
    await ctx.send('Test')


@client.command()
async def join(ctx, *, channel: discord.VoiceChannel = None):
    """Joins a voice channel"""

    if channel is None:
        channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    await channel.connect()


@client.command()
async def play(ctx, *, query):
    """Plays a file from the local filesystem"""
    await join(ctx=ctx, channel=None)

    if not query.__contains__(".mp3"):
        query = query + ".mp3"

    path = find_audio_file(query)
    #print(str(path) + str(query))
    if os.path.isfile(path + query):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path + query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(query))

    else:
        await ctx.send("Soundfile not found !")


@client.command(aliases=['maul', "fresse", "schnauze", "halt"])
async def stop(ctx):
    await ctx.voice_client.disconnect()


@client.command(aliases=['BIGMAC'])
async def bigmac(ctx, *, member: discord.Member):
    await play(ctx=ctx, query="BIGMAC")
    await asyncio.sleep(1.)
    await member.move_to(None)


async def raus(ctx: discord.ext.commands.Context):
    await asyncio.sleep(1.)
    await ctx.author.move_to(None)


@client.command(aliases=['soundfile', 'soundfiles'])
async def soundlist(ctx, query=None):
    list = "<:peepoClown:806233172564115467> SOUND-FILES <:peepoClown:806233172564115467>\n\n"

    if query is not None:

        if query.__contains__("meme"):
            query = "meme"
        elif query.__contains__("saufi"):
            query = "saufi"
        elif query.__contains__("sounds"):
            query = "sounds"
        else:
            existing_categories = ""
            pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles'))
            for i in range(len(pathfinder)):
                if not pathfinder[i].__contains__(".mp3") and not pathfinder[i] == "!bye":
                    existing_categories += pathfinder[i] + "\n"
            await ctx.send("Error: category not found.\n\nExisting categories:\n" + existing_categories)
            return

        pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles') + query)
        for i in range(len(pathfinder)):
            location = pathfinder[i].find(".mp3")
            list += pathfinder[i][:location] + "\n"
        await ctx.send(list)
    else:
        existing_categories = ""
        pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles'))
        for i in range(len(pathfinder)):
            if not pathfinder[i].__contains__(".mp3") and not pathfinder[i] == "!bye":
                existing_categories += pathfinder[i] + "\n"
        await ctx.send(f"\n Categories: \n{existing_categories}")


@client.command()
async def help(ctx):
    await ctx.send("<:peepoClown:806233172564115467> COMMANDS <:peepoClown:806233172564115467>\n\n" +
                   "!soundlist\n" +
                   "!soundlist KATEGORIE\n"
                   "!join\n" +
                   "!join CHANNELNAME\n" +
                   "!quit\n" +
                   "!bigmac USERNAME\n" +
                   "!help")


@client.command()
async def bye(ctx: discord.ext.commands.Context):
    pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles') + "!bye/")
    amount = len(pathfinder)
    sound_nr = random.randint(0, amount-1)
    audio = MP3(os.environ.get('Discord_Bot_Soundfiles') + "!bye/" + pathfinder[sound_nr])
    length = audio.info.length
    #await ctx.send(length)
    await play(ctx=ctx, query=pathfinder[sound_nr])
    await asyncio.sleep(length-1.5)
    await raus(ctx=ctx)



@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
   # print("test")
    if before.channel is None and after.channel is not None:
        onlyFans = discord.utils.get(member.guild.roles, name="OnlyFans")
        if onlyFans in member.roles:
            try:
                if not (client in member.voice.channel.members):
                    await member.voice.channel.connect()
            except:
                pass

            channel = discord.utils.get(client.voice_clients, channel=after.channel)
            path = find_audio_file("intro.mp3")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path + "intro.mp3"))
            await asyncio.sleep(0.3)
            channel.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        onlyFans = discord.utils.get(member.guild.roles, name="Erzfeind")
        if onlyFans in member.roles:
            try:
                if not (client in member.voice.channel.members):
                    await member.voice.channel.connect()
            except:
                pass

            channel = discord.utils.get(client.voice_clients, channel=after.channel)
            path = find_audio_file("ERZFEIND.mp3")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path + "ERZFEIND.mp3"))
            await asyncio.sleep(0.3)
            channel.play(source, after=lambda e: print('Player error: %s' % e) if e else None)


@client.command()
async def yt(ctx, *, url):
    await join(ctx=ctx)
    async with ctx.typing():
        await join(ctx=ctx)
        player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('Now playing: {}'.format(player.title))


class YTDLSource(discord.PCMVolumeTransformer):
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


@client.event
async def on_message(message):
    chatMessage = message.content

    print(message.author)
    print(message.content)

    if message.author == client.user:

        is_in_message = False
        for whitelist_label in temporary_whitelist_labels:
            if chatMessage.__contains__(whitelist_label):
                is_in_message = True
        if not is_in_message:
            await remove_message(message, 1.5)
        else:
            await remove_message(message, 30)
        return

    if chatMessage.__contains__(":peepoClown:"):
        await message.channel.send("<:peepoClown:806233172564115467>")

    await client.process_commands(message)

    if message.content.startswith('!'):
        await remove_message(message,  0.5)


async def remove_message(message, wait_duration):
    await asyncio.sleep(wait_duration)
    await message.delete()


def find_audio_file(sound_id):
    for root, dirs, files in os.walk(os.environ.get('Discord_Bot_Soundfiles'), topdown=True):
        for file in files:
            if file.casefold() == sound_id.casefold():
                return root + "\\"

