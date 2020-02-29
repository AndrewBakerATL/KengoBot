import discord
from discord.ext import commands
from itertools import cycle
from discord.ext import tasks

class Welcome(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # Commands

    @commands.command()
    async def binvite(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(color =  0xe22f32)
        invite = 'https://discordapp.com/api/oauth2/authorize?client_id=674619461470519323&permissions=8&scope=bot'
        embed.add_field(name='**Bot Invite: **', value="Here's your Kengo invite: {}. \nBe aware that this will only work if the bot is made public.".format(invite))
        await author.send(embed=embed)

def setup(client):
    client.add_cog(Welcome(client))
