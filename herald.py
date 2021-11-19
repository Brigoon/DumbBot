from helper import *
from pytube import YouTube
import pickle

class HeraldUser:
    def __init__(self, mp3Link_in, lastUseTime_in = 0, startTime_in = 0, duration_in = 30):
        self.mp3Link = mp3Link_in
        self.lastUseTime = lastUseTime_in
        self.startTime = startTime_in
        self.duration = duration_in

heraldDict = pickle.load(open("herald/heraldUsers.p", "rb"))

async def runHerald(ctx, link):
    if len(link) != 1:
        await ctx.send("A link is needed")
        return

    video = YouTube(link[0])
    stream = video.streams.filter(only_audio = True).first()
    stream.download("herald")

    if ctx.author.id in heraldDict.keys():
        #user exists
        await ctx.send("Audio updated!")
        heraldDict[ctx.author.id].mp3Link = "herald/"+video.title+".mp4"
    else:
        #new user
        await ctx.send("User initialized with new audio!")
        heraldDict[ctx.author.id] = HeraldUser("herald/"+video.title+".mp4")

    pickle.dump(heraldDict, open("herald/heraldUsers.p", "wb"))