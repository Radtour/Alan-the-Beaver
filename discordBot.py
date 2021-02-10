import asyncio
import discord
import os
from discord.ext import commands

#client = discord.Client()
intents = discord.Intents.default()
intents.voice_states = True
client = commands.Bot(command_prefix="!", help_command=None, intents=intents)

emoji_list = ["<:peepoClown:806233172564115467>"]

whitelist_labels = emoji_list + ["Existing categories"]


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

    path = os.environ.get('Discord_Bot_Soundfiles')
    print(path + query)
    if os.path.isfile(path + query):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(os.environ.get('Discord_Bot_Soundfiles') + query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(query))

    else:
        await ctx.send("Soundfile not found !")


@client.command(aliases=['BIGMAC'])
async def bigmac(ctx, *, member: discord.Member):
    await play(ctx=ctx, query="BIGMAC")
    time.sleep(1.)
    await member.move_to(None)


@client.command(aliases=['soundfile'])
async def soundlist(ctx, query):
    list = "<:peepoClown:806233172564115467> SOUND-FILES <:peepoClown:806233172564115467>\n\n"
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
            if not pathfinder[i].__contains__(".mp3"):
                existing_categories += pathfinder[i] + "\n"
        await ctx.send("Error: category not found.\n\nExisting categories:\n" + existing_categories)
        return

    pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles') + query)
    for i in range(len(pathfinder)):
        location = pathfinder[i].find(".mp3")
        list += pathfinder[i][:location] + "\n"
    await ctx.send(list)


@client.command()
async def help(ctx):
    await ctx.send("<:peepoClown:806233172564115467> COMMANDS <:peepoClown:806233172564115467>\n\n"+
          "!soundlist\n"+
          "!join\n"+
          "!join CHANNELNAME\n"+
          "!quit\n"+
          "!bigmac USERNAME\n"+
          "!help")


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
   # print("test")
    if before.channel is None and after.channel is not None:
        onlyFans = "OnlyFans"
        role = discord.utils.get(member.guild.roles, name= onlyFans)
        if role in member.roles:
            #print("test2")

            try:
                if not (client in member.voice.channel.members):
                    await member.voice.channel.connect()
            except:
                pass

            channel = discord.utils.get(client.voice_clients, channel=after.channel)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(os.environ.get('Discord_Bot_Soundfiles') + "intro.mp3"))
            await asyncio.sleep(0.3)
            channel.play(source, after=lambda e: print('Player error: %s' % e) if e else None)


@client.event
async def on_message(message):

    print(message.author)
    print(message.content)

    chatMessage = message.content

    if message.author == client.user:

        is_in_message = False
        for whitelist_label in whitelist_labels:
            if chatMessage.__contains__(whitelist_label):
                is_in_message = True
        if not is_in_message:
            await remove_message(message, 1.5)
        else:
            await remove_message(message, 5)
        return

    if chatMessage.__contains__(":peepoClown:"):
        await message.channel.send("<:peepoClown:806233172564115467>")

    await client.process_commands(message)

    if message.content.startswith('!'):
        await remove_message(message,  1.5)


async def remove_message(message, wait_duration):
    await asyncio.sleep(wait_duration)
    await message.delete()



