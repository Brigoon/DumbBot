from helper import *
from weather import *
from herald import *

client = discord.Client()
bot_prefix = "/"
bot = commands.Bot(command_prefix=bot_prefix)
regexp = re.compile('yee[e]*t')

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
		if regexp.search(ctx.content.lower()):
			await ctx.add_reaction('\N{EYES}')

		'''Send a custom message whenever stipe is mentioned'''
		if 'stipe' in ctx.content.lower():
			await ctx.channel.send('Stipe is a nugget')

		await bot.process_commands(ctx)

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
async def herald(ctx, *link):
	await runHerald(ctx, link)

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
