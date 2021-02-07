import discord
import random
import os
from discord.ext import commands
import asyncio

#client = discord.Client()
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def test(ctx):
    await ctx.send('Test')

#@client.command()
#async def play(ctx, file_path):
#    await ctx.send("Folgende Audio-Datei wird abgespielt: " + file_path)

@client.command()
async def vuvuzela(ctx):
    # grab the user who sent the command
    user = ctx.message.author
    voice_channel = user.voice.voice_channel
    channel = None
    # only play music if user is in a voice channel
    if voice_channel != None:
        # grab user's voice channel
        channel = voice_channel.name
        await client.say('User is in channel: ' + channel)
        # create StreamPlayer
        vc = await client.join_voice_channel(voice_channel)
        player = vc.create_ffmpeg_player('SPEICHER.mp3', after=lambda: print('done'))
        player.start()
        while not player.is_done():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        player.stop()
        await vc.disconnect()
    else:
        await client.say('User is not in a channel.')


@client.command()
async def join(ctx, *, channel: discord.VoiceChannel):
    """Joins a voice channel"""

    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    await channel.connect()

@client.command()
async def play(ctx, *, query):
    """Plays a file from the local filesystem"""

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(query))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    chatMessage = message.content

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if chatMessage.__contains__(":peepoClown:"):
        await message.channel.send("<:peepoClown:806233172564115467>")

    await client.process_commands(message)


