import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)
        await ctx.send("cleared **{}** messages...".format(amount))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(color = 0xfc4156)
        embed.add_field(name='**Purging Messages:**', value="**{}** messages being purged..".format(amount), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send("Kicking {} for {}".format(member.mention, reason))

    @commands.command(aliases=['bestowthehammer'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send('Banned {}'.format(member.mention))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command()
    async def mute(self, ctx, member : discord.Member, reason=None):
        roles = member.guild.roles
        muted = discord.utils.get(member.guild.roles, name='Kengo Muted')
        if muted in roles:
            await member.add_roles(muted)
            await ctx.send("User {} was muted for {}.".format(member.mention, reason))
        else:
            colour = discord.Colour(0x0e0e0f)
            await ctx.guild.create_role(reason='Mute Role', colour=colour, name='Kengo Muted', hoist=True)
            await member.add_roles(muted)
            await ctx.send("User {} was muted for {}.".format(member.mention, reason))

    @commands.command()
    async def unmute(self, ctx, member : discord.Member, reason=None):
        roles = member.roles
        muted = discord.utils.get(member.guild.roles, name='Kengo Muted')
        if muted in roles:
            await member.remove_roles(muted)
            await ctx.send("{} has been unmuted".format(member.mention))
        else:
            await ctx.send("{} is not muted".format(member.mention))

# Error Checking

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color = 0xfc4156)
            embed.add_field(name='**Error Check:**', value="Please specify amount.", inline=False)
            await ctx.send(embed=embed)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color = 0xfc4156)
            embed.add_field(name='**Error Check:**', value="Please specify amount.", inline=False)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Moderation(client))
