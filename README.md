# Dumb Bot

This is a project that started as a way for me to learn Python but has turned into a fun way to interact with friends.

## Dependencies

This bot uses various other Python libraries. Their names and versions will be up to date below:

discord.py - 1.7.3
aiohttp    - 3.7.4.post0
pytube     - 11.0.2
pydub      - 0.25.1
pytz       - 2019.3

## Usage

There is a shell script (for bash) included in this repository that will try to start the bot. If it doesn't start after 10 tries, it will wait 60 seconds. You can use this script simply by navigating to the containing folder and executing it:
```
./call.sh
```

Alternatively, if you would prefer to just call the bot without retries:
```
python3 dumbbot.py
```

## Commands

### help

To learn what the commands are, their usages, or valid input, use the 'help' command:
```
/help
```

You can also use it to see specific commands:
```
/help <command>
```

### herald

Herald allows you to control an intro audio (from YouTube) that will play whenever you join a voice channel (this can be configured to have a timer to make sure it doesn't get spammed).
To set an audio, use the 'herald' command:
```
/herald <link to youtube video>
```

The duration and start time can also be controlled:
```
/herald duration <time between 0 and 30 seconds>
/herald start <time between 0 and end of video>
```

Herald can be turned on/off:
```
/herald status <on or off>
```

### weather

Command to retrieve an official National Weather Service forecast. Currently, input can be either a city or exact latitude longitude coordinates. The next 6 timesteps are then printed:
```
/weather <latitude> <longitude>
```

### bet

This command will randomly choose 1 item among the items given as input:
```
/bet pizza chinese
```

To use this command with items with spaces in it, surround the items by quotes:
```
/bet "Play Rocket League" "Spend time with girlfriend"
```

###### NOTE: This command can be used for any number of inputs

### link

This is mainly used by me to keep track of websites I frequent:
```
/link <link abbreviation>
```

### clean

This command is only to be used by admins. This command will delete the last <N> messages:
```
/clean <N>
```

###### NOTE: 'clean' will not work if the messages are over 10 days old

## Other Tasks

This bot also performs some random tasks, either for hilarity or genuine usefullness.

### Link Reposting

Within my server, I keep a 'media' channel to keep pictures and links so it is easy to find previous posts. This bot will repost any links into the media channel.

### Channel Restriction

Within the media channel, and another channel we use for Stat Tracker bot, this bot will delete any content that is not supposed to be in those respective channels. The media channel only allows links and attachments, the stat_tracker channel only allows commands for Stat Tracker bot.

### Yeet Reaction

Whenever the word 'yeet' is typed in a message, the bot will respond with the :eyes: emoji. Again, we're dumb.

### Ratio Reaction

If the word 'ratio' is typed by itself, Dumbbot will support you by adding '+ you fell off + didn't ask'

## Under Construction

### Tracker Network Integration

We would like for the bot to be able to pull stats for various games that work with the Tracker Network.

### NFL Pick Em's

Pull all the NFL spreads every week and store everyones picks and can compare how everyone is doing.

## Authors

* **Brian Tomiuk**
* **Ty Dickinson**
