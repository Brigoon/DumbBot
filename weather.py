from helper import *
import requests

client = discord.Client()
bot_prefix = "/"
bot = commands.Bot(command_prefix=bot_prefix)

def _floatConvert(value):
    try:
        value = round(float(value), 4)
    except ValueError:
        pass
    return value

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
    if len(args) == 0:
        await ctx.send("Need at least one input, use 'help /weather'")
    elif len(args) > 2:
        await ctx.send("Oops, it looks like you entered more than 2 arguments, use 'help /weather'")
    else:
        try:
            cidx = args[0].index
            arg1, arg2 = args[0].split(',')
        except ValueError:
            if len(args) == 1:
                await ctx.send('Only one argument was entered. Please supply either: city,st or lat,lon.')
            else:
                arg1, arg2 = args.split(' ')

        arg2 = arg2.lsplit()
        arg1 = _floatConvert(arg1)
        arg2 = _floatConvert(arg2)

        if isinstance(arg1, float) and isinstance(arg2, float):
            lat = arg1
            lon = arg2
        elif isinstance(arg1, str) and isinstance(arg2, str):
            #FIXME: geocode city,st into lat/lon pair
            await ctx.send('Geocoding city, st into lat/lon coordinates is difficult and currently undergoing testing. Please enter lat/lon coordinates to get the forecast.')
        else:
            await ctx.send('The inputs are different types. Please enter two strings or two floats.')

    #we have to do 2 requests to get the forecast. the first is for a specific
    #lat/lon pair which returns the NWS grid box. Then, request again using
    #a slightly different link which specifies the box for the input lat/lon
    #FIXME: look into caching lat/lon pairs that may be input many times?
    #we can avoid 2 requests this way, allowing for slightly faster output
    #and worry less about rate limit
    page = requests.get(f'https://api.weather.gov/points/{lat},{lon}')
    if page.status_code != 200:
        await ctx.send(f'Something went wrong. For reference, the status code was: {page.status_code}. The NWS message was: {page.json()['detail']}.')
    page = requests.get(page.json()['properties']['forecast'])

    for i in page.json()['properties']['periods'][:6]:
        await ctx.send(f"{i['name']}: {i['detailedForecast']}")
