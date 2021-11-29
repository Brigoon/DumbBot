from helper import *
from pytube import YouTube
from pydub import AudioSegment
import pickle
import datetime

default_duration = 15
millisecond_conversion = 1000
wait_timer = 0

class HeraldUser:
    def __init__(self, mp3Link_in, startTime_in = 0, lastUseTime_in = None, duration_in = default_duration, audioLength_in = 0):
        self.mp3Link = mp3Link_in
        self.editedMp3Link = mp3Link_in
        self.startTime = startTime_in
        self.lastUseTime = lastUseTime_in
        self.duration = duration_in
        self.audioLength = audioLength_in

heraldDict = pickle.load(open("herald/heraldUsers.p", "rb"))

async def runHerald(ctx, args):
    if len(args) == 1:
        # If there is just a single argument then that argument must be a link

        # Download audio
        try:
            video = YouTube(args[0])
        except:
            await ctx.send("Not a valid YouTube link, run /herald link")
            return

        # Video cannot be longer than 10 minutes
        if video.length > 600:
            await ctx.send("Video is too long (greater than 10 minutes)")
            return

        stream = video.streams.filter(only_audio = True).first()
        stream.download("herald", filename = f'{ctx.author.id}.mp3')

        if ctx.author.id in heraldDict.keys():
            # User exists
            heraldDict[ctx.author.id].mp3Link = f'herald/{ctx.author.id}.mp3'
            await ctx.send("Herald updated")
        else:
            # New user
            heraldDict[ctx.author.id] = HeraldUser(f'herald/{ctx.author.id}.mp3')
            await ctx.send("User initialized with new Herald")

        # Ensure the playback does not last longer than possible
        if video.length < default_duration:
            heraldDict[ctx.author.id].duration = video.length
        else:
            heraldDict[ctx.author.id].duration = default_duration

        heraldDict[ctx.author.id].audioLength = video.length
        heraldDict[ctx.author.id].startTime = 0
        heraldDict[ctx.author.id].editedMp3Link = heraldDict[ctx.author.id].mp3Link

    elif len(args) == 2 and args[0] == 'duration':
        # If there are two arguments and the first is 'duration' then the user is
        # trying to update the duration of their audio

        if ctx.author.id in heraldDict.keys():
            # User exists
            duration = float(args[1])

            # Duration cannot be greater than 30
            if duration <= 30:

                # Duration cannot extend past the end of the audio so we adjust here
                if duration > heraldDict[ctx.author.id].audioLength - heraldDict[ctx.author.id].startTime:
                    heraldDict[ctx.author.id].duration = heraldDict[ctx.author.id].audioLength - heraldDict[ctx.author.id].startTime
                else:
                    heraldDict[ctx.author.id].duration = duration

                await ctx.send("Herald duration updated")

            else:
                await ctx.send("Duration must be less than or equal to 30 seconds")
                return
        else:
            # User does NOT exist so they need to first pick their audio
            await ctx.send("You do not have a chosen audio, run /herald link")
            return

    elif len(args) == 2 and args[0] == 'start':
        # If there are two arguments and the first is 'start' then the user is
        # trying to update the starting time of their audio

        if ctx.author.id in heraldDict.keys():
            # User exists
            start_time = float(args[1])

            # start_time cannot be greater than the audio length
            if start_time < heraldDict[ctx.author.id].audioLength:

                heraldDict[ctx.author.id].startTime = start_time
                audio = AudioSegment.from_file(heraldDict[ctx.author.id].mp3Link)

                # Create a new audio that starts at the desired time
                edited_audio = audio[start_time*millisecond_conversion:]

                edited_audio.export(f'herald/{ctx.author.id}_edited.mp3', format='mp3')
                heraldDict[ctx.author.id].editedMp3Link = f'herald/{ctx.author.id}_edited.mp3'

                # Need to adjust duration if the adjusted audio makes the duration extend past the audio length
                if (heraldDict[ctx.author.id].audioLength - start_time) < heraldDict[ctx.author.id].duration:
                    heraldDict[ctx.author.id].duration = heraldDict[ctx.author.id].audioLength - start_time

                await ctx.send("Start time updated")

            else:
                # The start time is greater than the length of the audio
                await ctx.send("The start time requested is beyond the end of the audio")
                return


        else:
            # User does NOT exist so they need to first pick their audio
            await ctx.send("You do not have a chosen audio, run /herald link")
            return

    elif len(args) == 2:
        # user used a flag that does not exist
        await ctx.send(f"Herald does not have a flag for '{args[0]}', run /herald link")
        return

    else:
        await ctx.send("A link is needed, run /herald link")
        return

    pickle.dump(heraldDict, open("herald/heraldUsers.p", "wb"))
    return

async def playHerald(member):

    # Only run if user has selected audio
    if member.id in heraldDict.keys():

        current_time = datetime.datetime.now()

        #only run if user has never joined voice channel or the time between joining exceeds delay
        if (isinstance(heraldDict[member.id], type(None))) or ((current_time - heraldDict[member.id].lastUseTime).total_seconds() > wait_timer):

            print(f'{member.name} has played Herald!')

            #set current time to use for future vc joins
            heraldDict[member.id].lastUseTime = current_time

            # Connect to voice channel
            time.sleep(0.5)
            vc = await member.voice.channel.connect()

            # Set and start audio
            audio = discord.FFmpegPCMAudio(heraldDict[member.id].editedMp3Link)
            time.sleep(0.5)
            vc.play(discord.PCMVolumeTransformer(audio, volume=0.7))

            # Wait for duration
            time.sleep(heraldDict[member.id].duration)

            # Stop and disconnect when done
            vc.stop()
            await vc.disconnect()

        else:
            pass

    pickle.dump(heraldDict, open("herald/heraldUsers.p", "wb"))
    return
