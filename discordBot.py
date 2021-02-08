import time

import discord
import random
import os
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


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


@client.command()
async def bigmac(ctx, *, member: discord.Member):
    await play(ctx=ctx, query="BIGMAC")
    time.sleep(1.5)
    await member.move_to(None)


@client.command()
async def soundlist(ctx):

    pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles'))
    for i in range(len(pathfinder)):
        await ctx.send(pathfinder[i])


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



