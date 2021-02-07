import discord
import random
from discord.ext import commands

#client = discord.Client()
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command
async def test(ctx):
    print("Test")
    await ctx.send("Test")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    chatMessage = message.content
   # check_for_audio(chatMessage)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if chatMessage.__contains__(":peepoClown:"):
        await message.channel.send("<:peepoClown:806233172564115467>")


#def check_for_audio(message):
    #if message.content.startswith('!play'):
        # Here it should be looked for the requested audio
