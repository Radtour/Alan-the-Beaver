import discord
import random

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    chatMessage = message.content

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if chatMessage.__contains__(":peepoClown:"):
        await message.channel.send("<:peepoClown:806233172564115467>")