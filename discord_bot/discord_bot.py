import asyncio
import discord
import os
from discord.ext import commands

from discord_bot.Audio import find_audio_file

intents = discord.Intents.default()
intents.voice_states = True
client = commands.Bot(command_prefix="!", help_command=None, intents=intents)

emoji_list = ["<:peepoClown:806233172564115467>"]

temporary_whitelist_labels = emoji_list + ["Existing categories", "Categories"]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    activity = discord.Activity(name="hunting with a cleaver", type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.command()
async def test(ctx):
    await ctx.send('Test')


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


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # print("test")
    if before.channel is None and after.channel is not None:
        only_fans = discord.utils.get(member.guild.roles, name="OnlyFans")
        if only_fans in member.roles:
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

        only_fans = discord.utils.get(member.guild.roles, name="Erzfeind")
        if only_fans in member.roles:
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


@client.event
async def on_message(message):
    chat_message = message.content

    print(message.author)
    print(message.content)

    if message.author == client.user:

        is_in_message = False
        for whitelist_label in temporary_whitelist_labels:
            if chat_message.__contains__(whitelist_label):
                is_in_message = True
        if not is_in_message:
            await remove_message(message, 1.5)
        else:
            await remove_message(message, 30)
        return

    if chat_message.__contains__(":peepoClown:"):
        await message.channel.send("<:peepoClown:806233172564115467>")

    await client.process_commands(message)

    if message.content.startswith('!'):
        await remove_message(message, 0.5)


async def remove_message(message, wait_duration):
    await asyncio.sleep(wait_duration)
    await message.delete()
