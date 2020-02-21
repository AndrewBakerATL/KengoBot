import discord
from discord.ext import commands
import random
import asyncio
import os
from itertools import cycle

# Command Prefix

client = commands.Bot(command_prefix = '!')

# Load Sequence

@client.command()
async def reload_moderation(ctx, extension):
    client.load_extension(f'moderation.{extension}')
    client.unload_extension(f'moderation.{extension}')

for filename in os.listdir('./checks'):
    if filename.endswith('.py'):
        client.load_extension(f'checks.{filename[:-3]}')

for filename in os.listdir('./nuclear'):
    if filename.endswith('.py'):
        client.load_extension(f'nuclear.{filename[:-3]}')

# for filename in os.listdir('./leveling'):
#     if filename.endswith('.py'):
#         client.load_extension(f'leveling.{filename[:-3]}')

for filename in os.listdir('./moderation'):
    if filename.endswith('.py'):
        client.load_extension(f'moderation.{filename[:-3]}')

for filename in os.listdir('./register'):
    if filename.endswith('.py'):
        client.load_extension(f'register.{filename[:-3]}')

for filename in os.listdir('./misc'):
    if filename.endswith('.py'):
        client.load_extension(f'misc.{filename[:-3]}')

# for filename in os.listdir('./streaming'):
#     if filename.endswith('.py'):
#         client.load_extension(f'streaming.{filename[:-3]}')

# Help Command

@client.command()
async def info(ctx):
    embed = discord.Embed(color = 0xfc4156)
    embed.set_author(name='Requesting Help Report', icon_url="https://cdn.discordapp.com/app-icons/481923206848970803/394817ba790d2fbb9c36715a7ec00576.png")
    embed.add_field(name='Introduction', value="For any major problems, please seek out the server staff. For any problems relating to the functioning of the bot, alert the creator of the problem and wait for a fix. The help menu consists of all commands relating to the server. Some of these commands may only be ran by a user with the appropriate rank. To see the commands, please check below.", inline=False)
    embed.add_field(name='__**Getting Started**__', value="Installing the bot.", inline=False)
    embed.add_field(name='Install Delta', value="!intro | Installs the bot's dependencies.", inline=False)
    embed.add_field(name='__**Moderation Commands**__', value="Use these to moderate the server", inline=False)
    embed.add_field(name='Ban User', value="!ban | Bans a user from the server, indefinitely.", inline=False)
    embed.add_field(name='Kick User', value="!kick | Kicks a user from the server.", inline=False)
    embed.add_field(name='Clear Messages', value="!clear (Number) | Clears a number of messages from the server.", inline=False)
    embed.add_field(name='Purge Messages', value="!purge (Number) | Purges a number of messages from the server.", inline=False)
    embed.add_field(name='Hammer User', value="!hammer | An advanced form of a ban deleting messages.", inline=False)
    embed.add_field(name='__**Information Commands**__', value="Use these to get information.", inline=False)
    embed.add_field(name='Identify User', value="!Identify (name) | Pulls a user's file from the server.", inline=False)
    embed.add_field(name='Server Information', value="!serverinfo | Shows information about the active server.", inline=False)
    embed.add_field(name='__**Music Commands**__', value="Music Playback Commands.", inline=False)
    embed.add_field(name='Play Song', value="!play (Terms) | Plays a song by the artist specified, or grabs the specific song.", inline=False)
    embed.add_field(name='Pause Song', value="!pause | Pauses the active playback.", inline=False)
    embed.add_field(name='Queue Song', value="!queue (Terms) | Adds a song into the queue.", inline=False)
    embed.add_field(name='Stop Song', value="!stop | Stops current playback.", inline=False)
    embed.add_field(name='Skip Song', value="!skip | Skips current playback.", inline=False)
    embed.add_field(name='Join Channel', value="!join | Bot joins your voice channel.", inline=False)
    embed.add_field(name='Leave Channel', value="!leave | Bot leaves your voice channel.", inline=False)
    embed.add_field(name='__**Verify Commands**__', value="Terms & Conditions.", inline=False)
    embed.add_field(name='Accept Terms', value="!accept | Accepts Terms of the Server and grants entry.", inline=False)
    embed.add_field(name='__**Miscellaneous Commands**__', value="Added on commands.", inline=False)
    embed.add_field(name='Echo Command', value="!echo (text) | The bot echoes the text given to it.", inline=False)
    embed.add_field(name='Ping Command', value="!ping | It replies back with pong.", inline=False)
    await ctx.author.send(embed=embed)
    await ctx.send('Information sent to {}...'.format(ctx.author.mention))


# Token Settings

Token = 'Token'
client.run(Token)
