from helper import *

client = discord.Client()
bot_prefix = "/"
bot = commands.Bot(command_prefix=bot_prefix)
regexp = re.compile('yee[e]*t')

@bot.event
async def on_ready():
	print("Bot Online!")

@bot.event
async def on_message(ctx):
	print('{} said:\"{}\" in #{}'.format(ctx.author.name, ctx.content, ctx.channel.name))

	if ctx.content.startswith('http') and ctx.author.id != 380935311540355072:
		channel = bot.get_channel(380028343611031565)
		await channel.send(ctx.content)
	elif (not ctx.content.startswith('http')) and ctx.channel.id == 380028343611031565 and not ctx.attachments:
		await ctx.delete()
	elif regexp.search(ctx.content.lower()):
		await ctx.add_reaction('\N{EYES}')
	
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
		await ctx.send('use \'/help link\' for valid links')

@bot.command()
async def bet(ctx, *args):
	'''YOU WANNA BET??
	<argn> nth bet string'''
	if len(args) > 1:
		await ctx.send(random.choice(args))
	else:
		await ctx.send('use \'/help bet\'')

"""@bot.command()
async def pokedex(ctx, name, gen, extra):
	'''Shows which Pokemon the user still needs to catch
	<arg1>:
	  brian: shows Brians needed pokemon
	  ty: shows Tys needed pokemon
	  both: shows what both Ty and Brian do not have
	  example: /pokedex brian
	<arg1> <arg2>:
	  <arg1> same as previous
	  <arg2> generation to be shown
	  example: /pokedex brian 1
	<arg1> <arg2>: adds a pokemon to the pokedex
	  <arg1> same as previous
	  <arg2> name of pokemon to be added
	  example: /pokedex brian bulbasaur
	<arg1> <arg2>: registers a new user
	  <arg1> register
	  <arg2> name of registee
	  example: /pokedex register brian'''
	
	'''
	Possibly some useful stuff instead of opening loads of textfiles:
	headers = ['approved','both_need','brian_dex','brian_need','jake_dex','jake_need',
	          'gen1','gen2','gen3','ty_dex','ty_need']
	path = r'C:\\Users\\Ty Dickinson\\DumbBot\\text'
	all_files = glob.glob(os.path.join(path, "*.txt"))
	list_of_dfs = [pd.read_csv(f,header=None) for f in all_files]
	combined_df = pd.concat(list_of_dfs, ignore_index=True,axis=1)
	combined_df.columns = headers

	combined_df.approved returns just the approved column.
	Since some files are longer than others, use .dropna() to only return
	data in the file. Another function that may be useful is .tolist().

	For example, you can replace dex = [dex1,dex2,dex3] with
	dex = combined_df.gen1.dropna().tolist() + combined_df.gen2.dropna().tolist() + combined_df.gen3.dropna().tolist()

	Since when someone adds a new pokemon, it is written to the textfile, it will be added to the combined_df
	the next time pokedex is called.
	'''

	run_pokedex(ctx, name, gen, extra)"""

@bot.command()
async def nuke(ctx):
	'''Only Brigoon can use this command
	removes all messages of a channel'''
	if ctx.author.id == 236886430616518666:
		if ctx.channel.id == 381186197965373440:
			await ctx.channel.purge(limit=100000000)
		else:
			await ctx.send('Wrong channel idiot')
	else:
		await ctx.send(ctx.author.id)

@bot.command()
async def clean(ctx, arg: int):
	'''Only Brigoon can use this command
	<arg> is number of lines to remove'''
	if ctx.author.id == 236886430616518666:
		await ctx.channel.purge(limit=arg)
	else:
		await ctx.send(ctx.author.id)

bot_ID_txt = open("text/bot_ID.txt","r")
bot_ID = bot_ID_txt.read()
bot_ID_txt.close()
bot.run(bot_ID)
