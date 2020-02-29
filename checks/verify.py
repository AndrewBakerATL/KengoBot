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
        game = discord.Game("Guarding the server...")
        await self.client.change_presence(status=discord.Status.dnd, activity=game)

# Commands

    @commands.command(aliases=['latency', 'speed'])
    async def ping(self, ctx):
        await ctx.send(f'Response Time: {round(self.client.latency * 1000)}ms')

def setup(client):
    client.add_cog(Verify(client))
