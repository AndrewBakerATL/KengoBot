import discord
from discord.ext import commands
from itertools import cycle
from discord.ext import tasks

class Echeck(commands.Cog):

    def __init__(self, client):
        self.client = client

# Error Checking

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            author = ctx.message.author
            embed = discord.Embed(color = 0xe22f32)
            embed.add_field(name='**Error Check: {}**'.format(author), value="Command not found. Please try again.")
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            author = ctx.message.author
            embed = discord.Embed(color = 0xe22f32)
            embed.add_field(name='**Error Check: {}**'.format(author), value="You don't have the permissions to execute this command.")
            await ctx.send(embed=embed)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color = 0xfc4156)
            embed.add_field(name='**Error Check:**', value="You're missing a required argument.", inline=False)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Echeck(client))
