import asyncio
import discord
from discord.ext import commands
import random
import os


class Roulette:
    player_list = []
    lobby_created = False

    @staticmethod
    async def get_func(message):
        if not Roulette.lobby_created and message.content.__contains__("create"):
            Roulette.lobby_created = True
            await Roulette.create(message)
        else:
            if message.content[1:] == "help":
                await gamemaster_help(message)
            elif message.content.__contains__("join"):
                await Roulette.join(message)
            elif message.content.__contains__("list"):
                if Roulette.lobby_created:
                    await Roulette.list_players(message)
                else:
                    await message.channel.send("Lobby first needs to be created !")
            else:
                await message.channel.send("Gamemaster-Command does not exist!\nCheck for commands with $help")

    @staticmethod
    async def create(message):
        Roulette.player_list.append(message.author.name)
        await message.channel.send(f"Lobby with {message.author.name} as leader got created")

    @staticmethod
    async def list_players(message):
        deathlist = 'Deathlist: \n'
        for i in range(len(Roulette.player_list)):
            deathlist += f"{Roulette.player_list[i]}\n"
        await message.channel.send(str(deathlist))

    @staticmethod
    async def join(message):
        Roulette.player_list.append(message.author.name)


async def gamemaster_help(message):
    helplist = [
        "Helplist-Gamemaster:\n" +
        "$join\n" +
        "$create\n" +
        "$start\n " +
        "$list"
    ]
    for i in range(len(helplist)):
        await message.channel.send(helplist[i])
