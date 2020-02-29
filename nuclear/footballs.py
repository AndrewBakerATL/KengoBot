# High Level Operations

import discord
from discord.ext import commands
from itertools import cycle
from discord.ext import tasks


class Footballs(commands.Cog):

    def __init__(self, client):
        self.client = client

# Event Logging

    @commands.command()
    async def nckick(self, ctx, key=None):
        idauthor = ctx.author.id
        idgowner = ctx.guild.owner.id
        Members = ctx.guild.members
        if idauthor == idgowner:
            if key == 'True':
                for Member in Members:
                    role = Member.top_role.position
                    bot = discord.utils.get(Member.guild.roles, name='PRIMEITE')
                    botp = bot.position
                    print("Member: {}, Role: {}, Position: {}, Bot Position: {}".format(Member, Member.top_role, role, botp))
                    if role < botp:
                        print("Kicked Member {}".format(Member))
                        await Member.kick(reason='Nuclear Kick Execution')
            elif key == None:
                await ctx.send("To confirm the Nuclear Kick, confirm the key by running the command again, followed by 'True'.")
            else:
                return
        else:
            await ctx.send(content="You're not authorized to use the Nuclear Command Structure (NCS). In fact, forget that it exists.", delete_after=10)

    @commands.command()
    async def ncban(self, ctx, key=None):
        idauthor = ctx.author.id
        idgowner = ctx.guild.owner.id
        Members = ctx.guild.members
        if idauthor == idgowner:
            if key == 'True':
                for Member in Members:
                    role = Member.top_role.position
                    bot = discord.utils.get(Member.guild.roles, name='PRIMEITE')
                    botp = bot.position
                    print("Member: {}, Role: {}, Position: {}, Bot Position: {}".format(Member, Member.top_role, role, botp))
                    if role < botp:
                        print("Kicked Member {}".format(Member))
                        await Member.ban(reason='Nuclear Kick Execution')
            elif key == None:
                await ctx.send("To confirm the Nuclear Ban, confirm the key by running the command again, followed by 'True'.")
            else:
                return
        else:
            await ctx.send(content="You're not authorized to use the Nuclear Command Structure (NCS). In fact, forget that it exists.", delete_after=10)

    @commands.command()
    async def ncwipe(self, ctx, key=None, amount=1000):
        idauthor = ctx.author.id
        idgowner = ctx.guild.owner.id
        channels = ctx.guild.text_channels
        if idauthor == idgowner:
            if key == 'True':
                for channel in channels:
                    await channel.purge(limit=amount, bulk=True)
                    embed = discord.Embed(color = 0xfc4156)
                    embed.add_field(name='**Nuclear Wipe:**', value="**{}** messages being purged..".format(amount), inline=False)
                    await channel.send(embed=embed)
            elif key == None:
                await ctx.send("To confirm the Nuclear Wipe, confirm the key by running the command again, followed by 'True'.")
            else:
                return
        else:
            await ctx.send(content="You're not authorized to use the Nuclear Command Structure (NCS). In fact, forget that it exists.", delete_after=10)

    @commands.command()
    async def ncpurge(self, ctx, key=None, amount=1000):
        idauthor = ctx.author.id
        idgowner = ctx.guild.owner.id
        if idauthor == idgowner:
            if key == 'True':
                await ctx.channel.purge(limit=amount)
                embed = discord.Embed(color = 0xfc4156)
                embed.add_field(name='**Nuclear Purge:**', value="**{}** messages being purged..".format(amount), inline=False)
                await ctx.send(embed=embed)
            elif key == None:
                await ctx.send("To confirm the Nuclear Purge, confirm the key by running the command again, followed by 'True'.")
            else:
                return
        else:
            await ctx.send(content="You're not authorized to use the Nuclear Command Structure (NCS). In fact, forget that it exists.", delete_after=10)

#    @commands.command()
#    async def overload(self, ctx, key=None, amount=1000):
#        channel = ctx.channel
#        for message in range(amount):
#            await channel.send("Overload Test")

def setup(client):
    client.add_cog(Footballs(client))
