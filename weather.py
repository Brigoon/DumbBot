from helper import *
import requests
import datetime
import pytz

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
async def run_weather(ctx, *args):
    if len(args) == 0:
        await ctx.send("Need to enter some geospatial location, use 'help /weather'")
    elif len(args) > 2:
        await ctx.send("Oops, it looks like you entered more than 2 arguments, use 'help /weather'")
    else:
        args = list(args) #convert from tuple to list to support assignment
        try:
            comma_index = args[0].index(",")
            args[0] = args[0][:comma_index]
            if len(args) == 1:
                args.extend(args[0][comma_index+1:])
        except ValueError:
            if len(args) == 1:
                await ctx.send('Only one argument was entered. Please supply either: city,st or lat,lon.')
                return

        arg0 = _floatConvert(args[0])
        arg1 = _floatConvert(args[1])

        if isinstance(arg0, float) and isinstance(arg1, float):
            lat = arg0
            lon = arg1
        elif isinstance(arg0, str) and isinstance(arg1, str):
            #FIXME: geocode city,st into lat/lon pair
            await ctx.send('Geocoding city, st into lat/lon coordinates is difficult and currently undergoing testing. Please enter lat/lon coordinates to get the forecast.')
            return
        else:
            await ctx.send('The inputs are different types. Please enter two strings or two floats.')
            return

        #we have to do 2 requests to get the forecast. the first is for a specific
        #lat/lon pair which returns the NWS grid box. Then, request again using
        #a slightly different link which specifies the box for the input lat/lon
        #FIXME: look into caching lat/lon pairs that may be input many times?
        #we can avoid 2 requests this way, allowing for slightly faster output
        #and worry less about rate limit

        page = requests.get(f'https://api.weather.gov/points/{lat},{lon}')
        timeZone = pytz.timezone(page.json()['properties']['timeZone'])
        if page.status_code != 200:
            await ctx.send(f'Something went wrong. For reference, the status code was: {page.status_code}. The NWS message was: {page.json()["detail"]}.')
            return
        page = requests.get(page.json()['properties']['forecast'])

        dateValid = datetime.datetime.strptime(page.json()['properties']['updated'], '%Y-%m-%dT%H:%M:%S%z')
        dateValid = dateValid.astimezone(timeZone)

        output = f"**Last Updated:** {dateValid.strftime('%A %d %B %Y %I:%M:%S%p')}\n"

        for i in page.json()['properties']['periods'][:6]:
            output += f"**{i['name']}:** {i['detailedForecast']}\n"

        await ctx.send(output)
