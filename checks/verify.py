import discord
from discord.ext import commands
from itertools import cycle
from discord.ext import tasks

class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Online')
        print("Bot Name: {}".format(self.client.user.name))
        print("Bot running under user: {}".format(self.client.user))
#        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game('...'))
        self.change_status.start()

    @tasks.loop(seconds=5)
    async def change_status(self):
        status = cycle(['Guarding the server..', 'Saving Servers...', 'Finding Bugs...'])
        await self.client.change_presence(activity=discord.Game(next(status)))

# Commands

    @commands.command(aliases=['latency', 'speed'])
    async def ping(self, ctx):
        await ctx.send(f'Response Time: {round(self.client.latency * 1000)}ms')

def setup(client):
    client.add_cog(Verify(client))
