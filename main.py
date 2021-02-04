# This is a sample Python script.
import os
from discordBot import client

client.run(os.environ.get('DISCORD_BOT'))

def find_bot():
    pathfinder = os.listdir("D:/Bot/")
    print(pathfinder[0])


def say_hello():
    print("Hello")
