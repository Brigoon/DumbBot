from helper import *
import requests
import datetime
import pytz
import io
import matplotlib.pyplot as plt

client = discord.Client()
bot_prefix = "/"
bot = commands.Bot(command_prefix=bot_prefix)

def _floatConvert(value):
    try:
        value = round(float(value), 4)
    except ValueError:
        pass
    return value

def _getLocation():
    return

def _savePlot(plot):
    data_stream = io.BytesIO()
    plot.savefig(data_stream, bbox_inches='tight', format='png', dpi=100)
    plt.close()

    data_stream.seek(0)
    pic = discord.File(data_stream,filename="fig.png")
    embed = discord.Embed(title="Title", description="Desc", color=0xeddce0)
    embed.set_image(url='attachment://fig.png')
    return pic, embed

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
        return

@bot.command()
async def make_plot(ctx):
    lat = 42.626023
    lon = -83.945811

    page = requests.get(f'https://api.weather.gov/points/{lat},{lon}')
    page = requests.get(page.json()['properties']['forecastHourly'])
    forecastInfo = page.json()['properties']['periods']

    temps = []
    dates = []
    for i in range(12):
        temps.append(forecastInfo[i]['temperature'])
        dates.append(datetime.datetime.strptime(forecastInfo[i]['startTime'], '%Y-%m-%dT%H:%M:%S%z'))

    dayOfWeek = [i.strftime('%A') for i in dates]
    timeOfDay = [i.strftime('%I') for i in dates]
    xticks = range(len(temps))

    #get min/max and round down/up to multiple of 5
    minTemp = min(temps)
    maxTemp = max(temps)
    minTemp = minTemp - (minTemp % 5)
    maxTemp = maxTemp + (5 - (maxTemp % 5))
    yticks = range(minTemp, maxTemp+1, 1)

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(1,1,1)
    plt.plot(xticks, temps, color='r', linestyle='-', marker='.', markersize=15)
    plt.xticks(ticks=xticks, labels=timeOfDay)
    plt.yticks(ticks=yticks)
    if len(set(dayOfWeek)) > 1:
        indexOfMidnight = timeOfDay.index('12')
        axesXLoc, _ = ax.transLimits.transform((indexOfMidnight, temps[0]))
        plt.axvline(x=indexOfMidnight, color='k', linestyle='--')
        plt.text(x=axesXLoc, y=1.0, s=dayOfWeek[indexOfMidnight], transform=ax.transAxes)
    plt.xlabel('Hour (12-h format)')
    plt.ylabel(r'Temperature $^\circ$F')

    plt.text(x=0.0, y=1.0, s=dayOfWeek[0], transform=ax.transAxes)
    plt.grid()
    plt.show()

    pic, embed = _savePlot(fig)
    await ctx.send(file=pic, embed=embed)
    return
