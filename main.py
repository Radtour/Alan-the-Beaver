# This is a sample Python script.
import os
import stat
from playsound import playsound
from discord import FFmpegPCMAudio, PCMVolumeTransformer

def look_for_direc():
    path = "D:/Bot/"
    if os.path.isdir(path):
        print("vorhanden")
        pathfinder = os.listdir("D:/Bot/")
        for i in range(len(pathfinder)):
            print(pathfinder[i])
    else:
        os.mkdir(path)
        os.chmod(path,  stat.S_IRWXO)


def play_sounds(path):
    playsound(path + "SPEICHER.mp3")


play_sounds("D:/Bot/")