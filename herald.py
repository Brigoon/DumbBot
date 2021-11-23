from helper import *
from pytube import YouTube
import pickle
from discord import FFmpegPCMAudio

class HeraldUser:
    def __init__(self, mp3Link_in, lastUseTime_in = 0, startTime_in = 0, duration_in = 15):
        self.mp3Link = mp3Link_in
        self.lastUseTime = lastUseTime_in
        self.startTime = startTime_in
        self.duration = duration_in

heraldDict = pickle.load(open("herald/heraldUsers.p", "rb"))

async def runHerald(ctx, args):
    if len(args) == 1:
        # If there is just a single argument then that argument must be a link

        # Download audio
        try:
            video = YouTube(args[0])
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

    elif len(args) == 2 and args[0] == 'duration':
        # If there are two arguments and the first is 'duration' then the user is
        # trying to update the duration of their audio

        if ctx.author.id in heraldDict.keys():
            # User exists
            duration = float(args[1])

            # Duration cannot be greater than 30
            if duration <= 30:
                heraldDict[ctx.author.id].duration = duration
                await ctx.send("Herald duration updated")
            else:
                await ctx.send("Duration must be less than or equal to 30 seconds")
                return
        else:
            # User does NOT exist so they need to first pick their audio
            await ctx.send("You do not have a chosen audio, run /herald link")
            return

    else:
        await ctx.send("A link is needed, run /herald link")
        return

    pickle.dump(heraldDict, open("herald/heraldUsers.p", "wb"))

async def playHerald(member):

    # Only run if user has selected audio
    if member.id in heraldDict.keys():

        # Connect to voice channel
        vc = await member.voice.channel.connect()

        # Set and start audio
        audio = FFmpegPCMAudio(heraldDict[member.id].mp3Link)
        vc.play(audio)

        # Wait for duration
        time.sleep(heraldDict[member.id].duration)

        # Stop and disconnect when done
        vc.stop()
        await vc.disconnect()