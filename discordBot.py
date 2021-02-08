import time

import discord
import random
import os
from discord.ext import commands
import asyncio

#client = discord.Client()
client = commands.Bot(command_prefix="!")

emoji_list = ["<:peepoClown:806233172564115467>"]

whitelist_labels = emoji_list + ["test"]

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
    list = "<:peepoClown:806233172564115467> SOUND-FILES <:peepoClown:806233172564115467>\n\n"
    pathfinder = os.listdir(os.environ.get('Discord_Bot_Soundfiles'))
    for i in range(len(pathfinder)):
        location = pathfinder[i].find(".mp3")
        list += pathfinder[i][:location] + "\n"
    await ctx.send(list)



@client.event
async def on_message(message):

    chatMessage = message.content

    if message.author == client.user:

        is_in_message = False
        for whitelist_label in whitelist_labels:
            if chatMessage.__contains__(whitelist_label):
                is_in_message = True
        if not is_in_message:
            time.sleep(1.5)
            await message.delete()
        return

    if chatMessage.__contains__(":peepoClown:"):
        await message.channel.send("<:peepoClown:806233172564115467>")

    await client.process_commands(message)

    if(message.content.startswith('!')):
        time.sleep(1.5)
        await message.delete()





