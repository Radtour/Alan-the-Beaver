import os
import ffmpeg
import discord
from discord.ext import commands


@bot.command(name="!play")
async def Test (ctx):

# Gets voice channel of message author
voice_channel = ctx.author.channel
channel = None
if voice_channel != None:
    channel = voice_channel.name
    vc = await voice_channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="D:/Bot/SPEICHER.mp3"))
    # Sleep while audio is playing.
    while vc.is_playing():
        sleep(.1)
    await vc.disconnect()
else:
    await ctx.send(str(ctx.author.name) + "is not in a channel.")
# Delete command after the audio is done playing.
await ctx.message.delete()