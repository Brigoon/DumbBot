from discord import channel
from helper import *
from weather import *
from herald import *

client = discord.Client()
bot_prefix = "/"
bot = commands.Bot(command_prefix=bot_prefix)
regexp_yeet = re.compile('yee[e]*t')
regexp_sheesh = re.compile('shee[e]*sh')

@bot.event
async def on_ready():
	print("Bot Online!")

@bot.event
async def on_message(ctx):
	'''Print all messages into console'''
	print(f'{ctx.author.name} said:\"{ctx.content}\" in #{ctx.channel.name}')

	'''Don't react to a message sent by the bot'''
	if ctx.author.id != 380935311540355072:

		'''Paste any link sent in private server to the media channel'''
		if ctx.content.startswith('http') and ctx.guild.id == 379321436478636034:
			channel = bot.get_channel(380028343611031565)
			await channel.send(ctx.content)

		'''Delete any message that is not a link in the media channel'''
		if (not ctx.content.startswith('http')) and ctx.channel.id == 380028343611031565 and not ctx.attachments:
			await ctx.delete()

		'''Add the :eyes: reaction to every message containing the word yeet'''
		if regexp_yeet.search(ctx.content.lower()):
			await ctx.add_reaction('\N{EYES}')

		'''Add the sheesh reaction to every message containing the word sheesh'''
		if regexp_sheesh.search(ctx.content.lower()):
			await ctx.add_reaction('<:sheesh:918963217722667038>')

		'''Send a custom message whenever stipe is mentioned'''
		if 'stipe' in ctx.content.lower():
			await ctx.channel.send('Stipe is a nugget')

		if ctx.content.lower() == 'ratio':
			await ctx.channel.send("+ you fell off + didn't ask")

		await bot.process_commands(ctx)

@bot.event
async def on_voice_state_update(member, before, after):
	'''Check that the bot is not the user connecting
		AND the user has entered a new voice channels
		AND the bot is not already in the voice channel'''
	if ( member.id != 380935311540355072
	     and before.channel != after.channel):
		await playHerald(member)

@bot.command()
async def link(ctx, flag = 'bad'):
	'''Provides the link desired
	<arg> which link you want. Links are:
	  api
	  rl
	  repo'''
	if flag == 'api':
		await ctx.send('https://discordpy.readthedocs.io/en/latest/api.html')
	elif flag == 'rl':
		await ctx.send('https://www.twitch.tv/rocketleague')
	elif flag == 'repo':
		await ctx.send('https://github.com/Brigoon/DumbBot')
	else:
		await ctx.send('Use \'/help link\' for valid links')

@bot.command()
async def bet(ctx, *args):
	'''Will randomly choose between at least 2 choices given.
	If the choices include any spaces (aka, more than just a single word)
	please surround them in quotes, ie:
	/bet "This is option 1" "This is option 2"'''
	if len(args) > 1:
		await ctx.send(random.choice(args))
	else:
		await ctx.send('Need at least 2 inputs, use \'/help bet\'')

@bot.command()
async def herald(ctx, *args):
	'''This is Herald, our friendly introduction officianado. To begin, give this command a YouTube
	link and from there you can change how long Herald will play the audio as well as what time in
	the audio it will start (example, a music video with a bunch of junk for the first 15 seconds).

	Arguments
	---------
	<link> :                        The YouTube link for you desired audio
	duration <time in seconds> :    How long you would like your audio to be played
	start <start time in seconds> : When you would like the audio to start'''

	await runHerald(ctx, args)

@bot.command()
async def weather(ctx, *args):
	'''Command to retrieve an official National Weather Service forecast. Currently,
	input can be either a city or exact latitude longitude coordinates. The next 6 timesteps
	are then printed.

	Arguments
	---------
	*args : string or float
		If float, input is latitude/longitude coordinates. Latitude should be in positive
		and longitude should be negative. If string, input is city which should have the format: city, st.
	'''
	await run_weather(ctx, *args)

@bot.command()
async def clean(ctx, arg: int = 25):
	'''Only Brigoon can use this command
	<arg> is number of lines to remove'''
	if ctx.author.id == 236886430616518666:
		await ctx.channel.purge(limit=arg)
	else:
		await ctx.send('Only Brigoon can use this command')

bot_ID_txt = open("text/bot_ID.txt","r")
bot_ID = bot_ID_txt.read()
bot_ID_txt.close()
bot.run(bot_ID)
