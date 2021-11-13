import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random

client = discord.Client()
bot_prefix = "/"
bot = commands.Bot(command_prefix=bot_prefix)

@bot.event
@asyncio.coroutine
def on_ready():
	print("Bot Online!")

@bot.event
@asyncio.coroutine
def on_message(message):
	print('{} said:\"{}\" in #{}'.format(message.author.name, message.content, message.channel.name))

	if message.content.startswith('http') and message.author.id != message.server.me.id:
		yield from bot.send_message(discord.Object(id='380028343611031565'), message.content)
	elif (not message.content.startswith('!')) and message.channel.id == '381123909556371456':
		if message.author.id != '190198409150464001':
			yield from bot.delete_message(message)
	elif (not message.content.startswith('http')) and message.channel.id == '380028343611031565':
		if not message.attachments:
			yield from bot.delete_message(message)
	elif 'yeet' in message.content.lower():
		yield from bot.add_reaction(message,'\N{EYES}')

	yield from bot.process_commands(message)

@bot.command()
@asyncio.coroutine
def link(*arg):
	'''Provides the link desired
	<arg> which link you want. Links are:
	  api
	  rl
	  ?
	  repo
	  nests
	  map (only works in ann arbor)'''
	if arg[0] == 'api':
		yield from bot.say('https://discordpy.readthedocs.io/en/latest/api.html')
	elif arg[0] == 'rl':
		yield from bot.say('https://www.twitch.tv/rocketleague')
	elif arg[0] == 'repo':
		yield from bot.say('https://github.com/Brigoon/DumbBot')
	elif arg[0] == 'nests':
		yield from bot.say('https://thesilphroad.com/atlas')
	else:
		yield from bot.say('use \'/help link\' for valid links')

@bot.command()
@asyncio.coroutine
def bet(*args):
	'''YOU WANNA BET??
	<argn> nth bet string'''
	if len(args) > 1:
		yield from bot.say(random.choice(args))
	else:
		yield from bot.say('use \'/help bet\'')

@bot.command()
@asyncio.coroutine
def pokedex(name='broken',gen='0',extra='0'):
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

	try:
		name = name.lower()
		gen = gen.lower()
		approved_file = open('text/approved.txt','r')
		approved = approved_file.readlines()
		approved_file.close()
		# Adds a new user to the approved list
		if name=='register':
			if gen+'\n' in approved:
				yield from bot.say(gen.title()+' has already been approved')
				return

			new_dex = open('text/'+gen+'_dex.txt','w')
			new_dex.close()
			new_approved = open('text/approved.txt','a')
			new_approved.write(gen+'\n')
			new_approved.close()
			yield from bot.say(gen.title()+' has been approved!')
			
		# Outputs what <arg1> needs with the option to restrict the generation
		elif gen=='0' or gen=='1' or gen=='2' or gen=='3':
			if not (((name+'\n') in approved) or name=='both'):
				yield from bot.say(name.title()+' is not a valid user')
				return

			need = open('text/'+name+'_need.txt','w')
			if gen=='0':
				dex1 = open('text/pokedex_gen1.txt','r')
				dex2 = open('text/pokedex_gen2.txt','r')
				dex3 = open('text/pokedex_gen3.txt','r')
				dex = [dex1, dex2, dex3]
			else:
				dex1 = open('text/pokedex_gen'+gen+'.txt','r')
				dex = [dex1]

			if name=='both':
				ty_dex = open('text/ty_dex.txt','r')
				brian_dex = open('text/brian_dex.txt','r')
				ty_cont = ty_dex.readlines()
				brian_cont = brian_dex.readlines()
				check = [ty_cont, brian_cont]
				ty_dex.close()
				brian_dex.close()
				addition = ''
			else:
				check_dex = open('text/'+name+'_dex.txt','r')
				cont = check_dex.readlines()
				check = [cont]
				check_dex.close()
				addition = 's'

			for i in range(len(dex)):
				if len(dex)>1:
					need.write('@@@@@@@@@@ GEN '+str(i+1)+' @@@@@@@@@@\n')
				for line in dex[i]:
					if len(check)==2:
						if not ((line in check[0]) or (line in check[1])):
							if 'mr. mime' in line:
								need.write('Mr. Mime\n')
							else:
								need.write(line.title())
					else:
						if not (line in check[0]):
							if 'mr. mime' in line:
								need.write('Mr. Mime\n')
							else:
								need.write(line.title())
				dex[i].close()
			need.close()

			need = open('text/'+name+'_need.txt','r')

			yield from bot.say(name.title()+' still need'+addition+':')
			read = need.read()
			need.close()
			if(len(read)==0):
				yield from bot.say('Nothing! You got all of them!')
			else:
				yield from bot.say(read)

		# Adds <arg2> to <arg1>s pokedex
		else:
			if not ((name+'\n') in approved):
				yield from bot.say(name.title()+' is not a valid user')
				return

			if extra != '0':
				gen = gen + ' ' + extra

			dex1 = open('text/pokedex_gen1.txt','r')
			dex2 = open('text/pokedex_gen2.txt','r')
			dex3 = open('text/pokedex_gen3.txt','r')
			dex = [dex1, dex2, dex3]

			pokemon = (gen+'\n')

			valid = False

			for i in range(len(dex)):
				if pokemon in dex[i]:
					valid = True
					break

			if valid:
				check_dex = open('text/'+name+'_dex.txt','r')
				check = check_dex.readlines()
				check_dex.close()

				if pokemon not in check:
					file = open('text/'+name+'_dex.txt','a')
					file.write(pokemon)
					file.close()
					yield from bot.say(pokemon.title().rstrip()+' has been succesfully added!')
				else:
					yield from bot.say(pokemon.title().rstrip()+' is already in '+name.title()+'\'s Pokedex')

			else:
				yield from bot.say(pokemon.title().rstrip()+' is not a valid Pokemon')

	except:
		yield from bot.say('use \'/help pokedex\'')
		raise

@bot.command(pass_context=True)
@asyncio.coroutine
def nuke(ctx):
	'''Only Brigoon can use this command
	removes all messages of a channel'''
	if ctx.message.author.id == '236886430616518666':
		if ctx.message.channel.name == 'test':
			yield from bot.purge_from(ctx.message.channel)
		else:
			yield from bot.say('Wrong channel idiot')

@bot.command(pass_context=True)
@asyncio.coroutine
def clean(ctx,arg):
	'''Only Brigoon can use this command
	<arg> is number of lines to remove'''
	if ctx.message.author.id == '236886430616518666':
		yield from bot.purge_from(ctx.message.channel,limit=int(arg))

bot_ID_txt = open("text/bot_ID.txt","r")
bot_ID = bot_ID_txt.read()
bot_ID_txt.close()
bot.run(bot_ID)
