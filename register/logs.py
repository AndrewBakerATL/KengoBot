import discord
from discord.ext import commands
from itertools import cycle
from discord.ext import tasks
from datetime import datetime

class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client

#    Commands

    @commands.command()
    async def logging(self, ctx, status):
        channels = ctx.guild.channels
        log = discord.utils.get(ctx.guild.channels, name='server-log')
        disabledlog = discord.utils.get(ctx.guild.channels, name='server-log-disabled')
        if status == 'Enable':
            if log in channels:
                await ctx.send("Logging Enabled.")
            elif disabledlog is not None:
                await disabledlog.edit(reason=None, name='server-log')
                await ctx.send("Logging Enabled.")
            else:
                await ctx.send("Enabling Server Log..")
                await ctx.guild.create_text_channel('server-log')
                await ctx.send("Logging Enabled.")
        if status == 'Disable':
            if log is not None:
                await log.edit(reason=None, name='server-log-disabled')
                await ctx.send("Logging Disabled.")
            if log is None:
                await ctx.send("Logging is not enabled.")

    @commands.command()
    async def log(self, ctx, type=None, *args):
        channels = ctx.guild.channels
        log = discord.utils.get(ctx.guild.channels, name='server-log')
        timestamp = ctx.message.created_at
        time = timestamp.replace(microsecond=0)
        if log in channels:
            if type == 'note':
                output = ''
                embed = discord.Embed(color = 0xe22f32)
                embed.add_field(name="**{}'s Note** | {}".format(ctx.author.name, time), value=" ".join(word for word in args), inline=False)
                await log.send(embed=embed)
            elif type == 'usernote':
                output = ''
                embed = discord.Embed(color = 0xe22f32)
                embed.add_field(name="**{}'s Note** | {}".format(ctx.author.name, time), value=" ".join(word for word in args), inline=False)
                await ctx.author.send(embed=embed)
            elif type is None:
                return
        elif log is None:
            await ctx.send("Logging is not enabled.")
        else:
            return

#    Event Logging

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, name='welcome')
        log = discord.utils.get(member.guild.channels, name='server-log')
        if channel is not None:
            gname = member.guild.name
            gicon = member.guild.icon_url
            avatar = member.avatar_url
            await channel.send("**Welcome To The Land** | *{}*".format(member))
            await channel.send("Welcome to the land, {}. We hope you enjoy your stay in {}. Channels are on the left, people are on the right.".format(member.mention, gname))
        elif channel == None:
            guild = member.guild
            await guild.create_text_channel('welcome')
            channel = discord.utils.get(member.guild.channels, name='welcome')
            await channel.send("**Welcome To The Land** | *{}*".format(member))
            await channel.send("Welcome to the land, {}. We hope you enjoy your stay in {}. Channels are on the left, people are on the right.".format(member.mention, gname))
        else:
            channel = member.guild.system_channel
            channel.send("Your server does not support this function.")

        if log is not None:
            gname = member.guild.name
            gicon = member.guild.icon_url
            avatar = member.avatar_url
            embed = discord.Embed(color = 0xe22f32)
            embed.set_author(name=gname, icon_url=gicon)
            embed.add_field(name='**User Joined:**', value="{} joined {}.".format(member, gname), inline=False)
            embed.add_field(name="**Author Name:**", value=member.name, inline=True)
            embed.add_field(name="**Author Username:**", value=member)
            embed.add_field(name="**Author ID:**", value=member.id, inline=False)
            embed.add_field(name="Created At:", value=member.created_at, inline=True)
            embed.add_field(name="Joined At:", value=member.joined_at, inline=True)
            embed.set_thumbnail(url=avatar)
            await log.send(embed=embed)
        if log is None:
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, name='welcome')
        log = discord.utils.get(member.guild.channels, name='server-log')
        if channel is not None:
            gname = member.guild.name
            gicon = member.guild.icon_url
            avatar = member.avatar_url
            await channel.send("**Leaving The Land** | *{}*".format(member))
            await channel.send("Leaving the land, {}? Our paths may cross again in the future. Channels are on the left, people are on the right.".format(member.mention, gname))
        elif channel == None:
            guild = member.guild
            await guild.create_text_channel('welcome')
            channel = discord.utils.get(member.guild.channels, name='welcome')
            await channel.send("**Leaving The Land** | *{}*".format(member))
            await channel.send("Leaving the land, {}? Our paths may cross again in the future..".format(member.mention, gname))
        else:
            channel = member.guild.system_channel
            channel.send("Your server does not support this function.")

        if log is not None:
            gname = member.guild.name
            gicon = member.guild.icon_url
            avatar = member.avatar_url
            embed = discord.Embed(color = 0xe22f32)
            embed.set_author(name=gname, icon_url=gicon)
            embed.add_field(name='**User Left:**', value="{} has left the land.".format(member.mention), inline=False)
            embed.set_thumbnail(url=avatar)
            await log.send(embed=embed)
        if log is None:
            return

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        owner = guild.owner
        gicon = guild.icon_url
        gname = guild.name
        colour = discord.Colour(0xcc282b)
        await guild.create_role(name='Kengo bot', colour=colour, hoist=True, mentionable=True)
        embed = discord.Embed(color = 0xe22f32)
        embed.set_author(name='Notice of Installation | {}'.format(owner.name), icon_url="{}".format(gicon))
        embed.add_field(name='Your New Bot', value="Congratulations. Either you or someone on your team recently added KengoBot to the server. If you didn't mean to do this, please remove the bot. Rest assured that there's no malicious code in the bot's structure. You can pull the command list by typing !help into the applicable server.", inline=False)
        await owner.send(embed=embed)
        embed = discord.Embed(color = 0xe22f32)
        embed.set_author(name='Your Nuclear Command Structure (NCS) | {}'.format(owner), icon_url="{}".format(gicon))
        embed.add_field(name="Nuclear Information", value="As the server owner, this information is only sent to you. There is no other way to request it. This is the only copy. No other user may request it, unless they're instated as the server owner by Discord. These commands can only be ran by you. There are redundant hard-coded logic checks, based on ID confirmation, which prevents anyone else from initiating them, regardless of their permissions structure, role, status, or rank.", inline=False)
        embed.add_field(name="Nuclear Footballs", value="Your Nuclear Commands", inline=False)
        embed.add_field(name="Nuclear Kick | !nckick", value="The NCS Kick Command. Kick every user in the server below the bot in terms of server hierarchy, irrelevant of permissions structure.", inline=False)
        embed.add_field(name="Nuclear Ban | !ncban", value="The NCS Ban Command. Ban every user in the server below the bot in terms of server hierarchy, irrelevant of permissions structure.", inline=False)
        embed.add_field(name="Nuclear Wipe | !ncwipe", value="The NCS Wipe Command. Wipe the chat history of every text-based channel in the server. The number defaults to 1,000, but will act according to manual spec as well.", inline=False)
        embed.add_field(name="Nuclear Purge | !ncpurge", value="The NCS Purge Command. Purge the chat history of the current channel in the server. The number defaults to 1,000, but will act according to manual spec as well.", inline=False)
        embed.set_footer(text="Nuclear Command Structure")
        await owner.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log = discord.utils.get(message.guild.channels, name='server-log')
        if log is not None:
            gname = message.guild.name
            gicon = message.guild.icon_url
            avatar = message.author.avatar_url
            author = message.author
            content = message.content
            channel = message.channel
            embed = discord.Embed(color = 0xe22f32)
            embed.set_author(name=gname, icon_url=gicon)
            embed.add_field(name='**Message Deleted:**', value="A message was deleted in {} by {}.".format(channel, author.name), inline=False)
            embed.add_field(name="**Author Name:**", value=author.name, inline=True)
            embed.add_field(name="**Author Username:**", value=author)
            embed.add_field(name="**Author ID:**", value=author.id, inline=False)
            embed.add_field(name="**Message Content:**", value=content)
            embed.set_thumbnail(url=avatar)
            await log.send(embed=embed)
        if log is None:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log = discord.utils.get(before.guild.channels, name='server-log')
        channel = before.channel
        gname = before.guild.name
        gicon = before.guild.icon_url
        avatar = before.author.avatar_url
        if log is not None:
            embed = discord.Embed(title="Message Edited", description="A message was edited by *{}* in *{}*.".format(before.author.name, channel), color = 0xe22f32)
            embed.set_author(name=gname, icon_url=gicon)
            embed.add_field(name="**Author Name:**", value=before.author.name, inline=True)
            embed.add_field(name="**Author Username:**", value=before.author, inline=True)
            embed.add_field(name="**Author ID:**", value=before.author.id, inline=False)
            embed.add_field(name="**Message Before:**", value=before.content, inline=True)
            embed.add_field(name="**Message After:**", value=after.content, inline=True)
            embed.set_thumbnail(url=avatar)
            await log.send(embed=embed)
        if log is None:
            return

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        log = discord.utils.get(member.guild.channels, name='server-log')
        if log is not None:
            gname = member.guild.name
            gicon = member.guild.icon_url
            avatar = member.avatar_url
            embed = discord.Embed(title="**User Banned**", description="{} was banned from the server.".format(member.mention), color = 0xe22f32)
            embed.set_author(name=gname, icon_url=gicon)
            embed.add_field(name='**Name:**', value=member.name, inline=True)
            embed.add_field(name="**Username:**", value=member, inline=True)
            embed.add_field(name="**User ID:**", value=member.id, inline=True)
            embed.set_thumbnail(url=avatar)
            await log.send(embed=embed)
        if log is None:
            return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        log = discord.utils.get(before.guild.channels, name='server-log')
        if log is not None:
            if before.status != after.status:
                user = before.mention
                embed = discord.Embed(title='**Status Change** | :eyes: ', description="{}'s status changed".format(user), color=0xfc4156)
                embed.add_field(name="**Changed To**", value="Member's status changed from **{}** to **{}**".format(before.status, after.status))
                embed.set_thumbnail(url=before.avatar_url)
                embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
                embed.set_footer(text="Delta Data Report")
                await log.send(embed=embed)
            if before.activity != after.activity:
                user = before.mention
                embed = discord.Embed(title='**Game Changed** | :joystick: ', description="{}'s playing a new game".format(user), color=0xfc4156)
                embed.add_field(name="**Changed To**", value="Member's game changed from **{}** to **{}**".format(before.game, after.game))
                embed.set_thumbnail(url=before.avatar_url)
                embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
                embed.set_footer(text="Delta Data Report")
                await log.send(embed=embed)
            if before.nick != after.nick:
                user = before.mention
                embed = discord.Embed(title='**Name Changed** | :pencil: ', description="{}'s name changed".format(user), color=0xfc4156)
                embed.add_field(name="**Username**", value=before.name)
                embed.add_field(name="**Changed To**", value="Member's name changed from **{}** to **{}**".format(before.nick, after.nick))
                embed.set_thumbnail(url=before.avatar_url)
                embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
                embed.set_footer(text="Delta Data Report")
                await log.send(embed=embed)
            if before.top_role != after.top_role:
                roles = after.roles
                user = before.mention
                embed = discord.Embed(title='**Role Changed** | :briefcase: ', description="{}'s role changed".format(user), color=0xfc4156)
                embed.add_field(name="**Username**", value=before.name)
                embed.add_field(name="**Changed To**", value="Member's role changed from **{}** to **{}**".format(before.top_role, after.top_role))
                embed.add_field(name="**Held Roles**", value=", ".join([role.name for role in roles]))
                embed.set_thumbnail(url=before.avatar_url)
                embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
                embed.set_footer(text="Delta Data Report")
                await log.send(embed=embed)
            if before.avatar_url != after.avatar_url:
                user = before.mention
                embed = discord.Embed(title='**Avatar Changed** | :eyes: ', description="{}'s changed their avatar".format(user), color=0xfc4156)
                embed.add_field(name="**Username**", value=before.name)
                embed.set_thumbnail(url=before.avatar_url)
                embed.set_author(name="Logging Change", icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
                embed.set_footer(text="Delta Data Report")
                await log.send(embed=embed)
                embed.set_thumbnail(url=after.avatar_url)
                await log.send(embed=embed)
        if log is None:
            return

#   Error Checking

    @logging.error
    async def logging_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color = 0xfc4156)
            embed.add_field(name='**Logging Error:**', value="Please include either 'Enable' or 'Disable'.", inline=False)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Logs(client))
