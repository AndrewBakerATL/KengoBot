# Tenor Gif Tracking

import discord
from discord.ext import commands
from itertools import cycle
from discord.ext import tasks
import requests
import json
from apiclient.discovery import build

class Serv(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands

    @commands.command()
    async def gif(self, ctx, search, *, src=None):
        apikey = 'D52NGBGYP6OC' # Tenor API Key
        lmt = 1
        gsearch = requests.get("https://api.tenor.com/v1/search?q={}&key={}&limit={}".format(search, apikey, lmt)).json()
        gif = gsearch['results'][0]['media'][0]['mediumgif']['url']
        if src == None:
            embed = discord.Embed(color = 0xe22f32)
            embed.add_field(name='GIF', value="{}'s {}\n".format(ctx.message.author.mention, search))
            embed.set_image(url=gif)
            await ctx.send(embed=embed)
        elif src == 'source':
            embed = discord.Embed(color = 0xe22f32)
            embed.add_field(name='GIF', value="{}'s {} \n {}".format(ctx.message.author.mention, search, gif))
            embed.set_image(url=gif)
            await ctx.send(embed=embed)

    @commands.command()
    async def gify(self, ctx, *, search):
        apikey = "qcnLJ2yZ44Yv2arIR4mjmkpN2HpJYhYf"
        lmt = 1
        gysearch = requests.get("http://api.giphy.com/v1/gifs/search?q=c{}&key={}&limit=1".format(search, apikey, lmt)).json()
        gify = gysearch['data'][0]['images']['downsized_large']['url']
        embed = discord.Embed(color = 0xe22f32)
        embed.add_field(name='GIFY', value="{}'s {} \n {}".format(ctx.message.author.mention, search, gify))
        embed.set_image(url=gify)
        await ctx.send(embed=embed)

    @commands.command()
    async def wcurrent(self, ctx, *, city):
        apikey = "1dc640040ee024eb670533b47f754197"
        uni = 'imperial'
        wsearch = requests.get("http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units={}".format(city, apikey, uni)).json()
        coordlon = wsearch['coord']['lon']
        coordlat = wsearch['coord']['lat']
        mweather = wsearch['weather'][0]['main']
        dweather = wsearch['weather'][0]['description']
        mtemp = wsearch['main']['temp']
        ftemp = wsearch['main']['feels_like']
        hitemp = wsearch['main']['temp_max']
        lotemp = wsearch['main']['temp_min']
        humid = wsearch['main']['humidity']
        locale = wsearch['name']
        country = wsearch['sys']['country']
        mcunit = 5/9*(mtemp-32)
        fcunit = 5/9*(ftemp-32)
        hicunit = 5/9*(hitemp-32)
        locunit = 5/9*(lotemp-32)
        embed = discord.Embed(color = 0xe22f32)
        embed.set_footer(text='Weather Report')
        embed.add_field(name='***Coordinates***', value='Geolocation', inline=False)
        embed.add_field(name='Longitude:', value=coordlon, inline=True)
        embed.add_field(name='Latitude:', value=coordlat, inline=True)
        embed.add_field(name='***Weather***', value="{}, {}".format(locale, country), inline=False)
        embed.add_field(name='Main', value=mweather.capitalize(), inline=True)
        embed.add_field(name='Description', value=dweather.capitalize(), inline=True)
        embed.add_field(name='***Temperature***', value='Data', inline=False)
        embed.add_field(name='Main:', value="{}°F ({}°C)".format(mtemp, round(mcunit, 2)), inline=True)
        embed.add_field(name="Feels Like:", value="{}°F ({}°C)".format(ftemp, round(fcunit, 2)), inline=True)
        embed.add_field(name="Humidity:", value="{}%".format(humid), inline=True)
        embed.add_field(name="Hi:", value="{}°F ({}°C)".format(hitemp, round(hicunit, 2)), inline=True)
        embed.add_field(name="Low:", value="{}°F ({}°C)".format(lotemp, round(locunit, 2)), inline=True)
        embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fcdn3.iconfinder.com%2Fdata%2Ficons%2Fweather-and-forecast%2F51%2FWeather_icons_grey-03-512.png")
        embed.set_author(name='Kengo Weather | Current')
        await ctx.send(embed=embed)

    @commands.command()
    async def google(self, ctx, *, term):
        apikey = 'AIzaSyCEvzIKceBq4ViLLbxcXCihobXtfr7mhQc'
        resource = build("customsearch", 'v1', developerKey=apikey).cse()
        result = resource.list(q='{}'.format(term), cx='003797154308276670266:zw8o82b3drt').execute()
        results = result['items'][0]
        image = results['pagemap']['cse_thumbnail'][0]['src']
        embed = discord.Embed(color = 0xe22f32)
        embed.set_footer(text='Google Search')
        embed.add_field(name="**Top Result: {}**".format(results['title']), value=results['link'])
        embed.set_thumbnail(url="{}".format(image))
        await ctx.send(embed=embed)

    @commands.command()
    async def glist(self, ctx, *, term):
        apikey = 'AIzaSyCEvzIKceBq4ViLLbxcXCihobXtfr7mhQc'
        resource = build("customsearch", 'v1', developerKey=apikey).cse()
        result = resource.list(q='{}'.format(term), cx='003797154308276670266:zw8o82b3drt').execute()
        results = result['items']
        embed = discord.Embed(color = 0xe22f32)
        embed.set_footer(text='Google Search')
        for item in results:
            embed.add_field(name="**Search Entry: {}**".format(item['title']), value="{}\n{}\n \n ".format(item['link'], item['snippet']), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def img(self, ctx, *, term):
        apikey = 'AIzaSyCEvzIKceBq4ViLLbxcXCihobXtfr7mhQc'
        resource = build("customsearch", 'v1', developerKey=apikey).cse()
        result = resource.list(q='{}'.format(term), cx='003797154308276670266:zw8o82b3drt', searchType='image').execute()
        results = result['items'][0]['link']
        embed = discord.Embed(color = 0xe22f32)
        embed.set_footer(text='Google Images')
        embed.set_image(url=results)
        await ctx.send(embed=embed)

    @commands.command()
    async def notify(self, ctx, type):
        if type == 'active':
            author = ctx.author
            groles = ctx.guild.roles
            active = discord.utils.get(ctx.guild.roles, name='Active')
            if active in groles:
                await author.add_roles(active)
                await ctx.send('Notifications Enabled.')
            else:
                colour = discord.Colour(0xcc282b)
                await ctx.guild.create_role(reason='Notify Role', colour=colour, name='Active', hoist=False, mentionable=True)
                await author.add_roles(active)
                await ctx.send('Notifications Enabled.')
        elif type == 'inactive':
            author = ctx.author
            groles = ctx.guild.roles
            aroles = ctx.author.roles
            active = discord.utils.get(ctx.guild.roles, name='Active')
            if active in aroles:
                await author.remove_roles(active)
                await ctx.send('Notifications Disabled.')
            else:
                await ctx.send("You're not Active.")

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain',
                     'Definitely, no question',
                     'Count on it, for sure',
                     'From what I know, yeah',
                     'Sure, why not?',
                     'Most likely',
                     'It looks good',
                     'Yes',
                     'A little hazy',
                     'Maybe, not really sure',
                     'Ask again later',
                     'Are you serious?',
                     'Uh, why?',
                     'Not looking good',
                     'Cannot predict it',
                     "Don't count on it",
                     'My sources say no',
                     "It's doubtful."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    # Error Checking

    @notify.error
    async def notify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color = 0xfc4156)
            embed.add_field(name='**Error Check:**', value="Please set notifications to either 'Active' or 'Inactive'.", inline=False)
            await ctx.send(embed=embed)

    @gif.error
    async def gif_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color = 0xfc4156)
            embed.add_field(name='**GIF Error:**', value="Please input a search term, or phrase using quotes.", inline=False)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Serv(client))
