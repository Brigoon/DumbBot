from helper import *
from pytube import YouTube
import pickle
from os.path import exists

class HeraldUser:
    def __init__(self, mp3Link_in, lastUseTime_in = 0, startTime_in = 0, duration_in = 15):
        self.mp3Link = mp3Link_in
        self.lastUseTime = lastUseTime_in
        self.startTime = startTime_in
        self.duration = duration_in

heraldDict = pickle.load(open("herald/heraldUsers.p", "rb"))

async def runHerald(ctx, *args):
    if len(args[0]) == 1:
        # If there is just a single argument then that argument must be a link

        # Download audio
        try:
            video = YouTube(args[0][0])
        except:
            await ctx.send("Not a valid YouTube link")
            return
        
        stream = video.streams.filter(only_audio = True).first()
        stream.download("herald", filename = f'{ctx.author.id}_audio.mp3')

        if ctx.author.id in heraldDict.keys():
            # User exists
            heraldDict[ctx.author.id].mp3Link = f'herald/{ctx.author.id}_audio.mp3'
            await ctx.send("Herald updated")
        else:
            # New user
            heraldDict[ctx.author.id] = HeraldUser(f'herald/{ctx.author.id}_audio.mp3')
            await ctx.send("User initialized with new Herald")

    elif len(args[0]) == 2 and args[0][0] == 'duration':
        # If there are two arguments and the first is 'duration' then the user is
        # trying to update the duration of their audio

        if ctx.author.id in heraldDict.keys():
            # User exists
            heraldDict[ctx.author.id].duration = args[0][1]
            await ctx.send("Herald duration updated")
        else:
            # User does NOT exist so they need to first pick their audio
            await ctx.send("You do not have a chosen audio, run /herald link")
            return

    elif len(args[0]) == 2 and args[0][0] == 'start':
        # If there are two arguments and the first is 'start' then the user is
        # trying to update the start time of their audio

        if ctx.author.id in heraldDict.keys():
            # User exists
            heraldDict[ctx.author.id].startTime = args[0][1]
            await ctx.send("Herald start time updated")
        else:
            # User does NOT exist so they need to first pick their audio
            await ctx.send("You do not have a chosen audio, run /herald link")
            return

    else:
        await ctx.send("A link is needed, run /herald link")
        return

    pickle.dump(heraldDict, open("herald/heraldUsers.p", "wb"))