# Dumb Bot

This is a project that started as a way for me to learn Python. I also thought it would be fun to mess around with a Pokedex tracker for keeping track of what you still need in PokemonGo. That is now it's primary use.

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

### pokedex

This command will keep track of and update your personal Pokemon Go pokedex. To get started use the 'register' command:
```
/pokedex register <username>
```

After you have registered your name, you can add pokemon using the following syntax:
```
/pokedex <username> <pokemon>
```

To view what you still need:
```
/pokedex <username>
```
###### NOTE: If you have not added enough Pokemon to your Pokedex, this will not work, as Discord only allows up to 2000 characters to be printed per message.

To view what you still need within a specific generation:
```
/pokedex <username> <generation>
```

### bet

This command will randomly choose 1 item among the items given as input:
```
/bet pizza chinese
```

To use this command with items with spaces in it, surround the items by quotes:
```
/bet "Play Pokemon Go" "Spend time with girlfriend"
```

###### NOTE: This command can be used for any number of inputs

### link

This is mainly used by me to keep track of websites I frequent:
```
/link <link abbreviation>
```

### nuke

This is only to be used by admins. This will clear out an entire channel. I mainly use it within my test channels when debugging new commands:
```
/nuke
```

### clean

Similar to nuke, this command is only to be used by admins. This command will delete the last <N> messages:
```
/clean <N>
```

###### NOTE: 'nuke' and 'clean' will not work if the messages are over 10 days old

## Other Tasks

This bot also performs some random tasks, either for hilarity or genuine usefullness.

### Link Reposting

Within my server, I keep a 'media' channel to keep pictures and links so it is easy to find previous posts. This bot will repost any links into the media channel.

### Channel Restriction

Within the media channel, and another channel we use for Stat Tracker bot, this bot will delete any content that is not supposed to be in those respective channels. The media channel only allows links and attachments, the stat_tracker channel only allows commands for Stat Tracker bot.

### Yeet Reaction

Whenever the word 'yeet' is typed in a message, the bot will respond with the :eyes: emoji. Again, we're dumb.

## Under Construction

### Attachment Reposting

I am currently *trying* to have the bot repost any attachments into the media channel as well. This requires the use of the aiohttp module so I am trying to understand how that works.

## Authors

* **Brian Tomiuk**
* **Ty Dickinson**
