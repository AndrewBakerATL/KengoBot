import discord
import wavelink
from discord.ext import commands

queue = []

class Client(commands.Cog):

    def __init__(self):
        super(client, self).__init__(command_prefix=['audio ', 'wave ','aw '])

        self.add_cog(Music(self))

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

        if not hasattr(client, 'wavelink'):
            self.client.wavelink = wavelink.Client(self.client)

        self.client.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.client.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.client.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='us_central')

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.client.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        player = self.client.wavelink.get_player(ctx.guild.id)
        if query == 'queue':
            track = queue[0]
            queued = queue[1:]
            embed = discord.Embed(title="**Playing Music**", description="Playing Active Queue", color = 0xe22f32)
            embed.add_field(name="***Now Playing***", value="{}".format(queue[0]), inline=True)
            embed.add_field(name="***Up Next***", value="{}".format(queued[0]), inline=True)
            embed.set_thumbnail(url=str(track.thumb))
            if queue is not None:
                embed.add_field(name="**Song Queue**", value=", ".join([str(track) for track in queued]), inline=False)
            elif queue == None:
                embed.add_field(name="**Song Queue**", value="The queue is empty...", inline=False)

            await ctx.send(embed=embed)
            await player.play(queue[0])

        else:
            tracks = await self.client.wavelink.get_tracks(f'ytsearch:{query}')

            if not tracks:
                return await ctx.send('Could not find any songs with that query.')

            if not player.is_connected:
                await ctx.invoke(self.connect_)

            await ctx.send(f'Added {str(tracks[0])} to the queue.')

            embed = discord.Embed(title="**Playing Music**", description="Playing Active Queue", color = 0xe22f32)


            await player.play(tracks[0])

    @commands.command()
    async def queue(self, ctx, *, query: str):
        tracks = await self.client.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.client.wavelink.get_player(ctx.guild.id)

        # await ctx.send(f'Added {str(tracks[0])} to the queue.')
            # print("Name: {} | Length: {} | URL: {}".format(player.title, round(player.length/60000, 2), player.uri))
        queue.append(tracks[0])
        await ctx.send("Queued Song")

    @commands.command()
    async def queued(self, ctx):
        if queue is not None:
            print(", ".join([str(track) for track in queue]))
        if queue is None:
            print("The queue uis empty")

    @commands.command()
    async def leave(self, ctx):
        server = ctx.guild
        voice_client = server.voice_client
        player = self.client.wavelink.get_player(ctx.guild.id)
        if player.is_connected:
            await player.disconnect()
            print("Bot left the voice channel")
        else:
            print("Bot was not in channel")

    @commands.command()
    async def pause(self, ctx):
        server = ctx.guild
        voice_client = server.voice_client
        player = self.client.wavelink.get_player(ctx.guild.id)
        if player.is_playing:
            await player.set_pause(pause=True)
            embed = discord.Embed(color = 0xe22f32)
            embed.add_field(name="**Music Playback**", value="Paused music playback..", inline=True)
            embed.set_footer(text="Kengo System")
            await ctx.send(embed=embed)

    @commands.command()
    async def resume(self, ctx):
        server = ctx.guild
        voice_client = server.voice_client
        player = self.client.wavelink.get_player(ctx.guild.id)
        if player.is_paused:
            await player.set_pause(pause=False)
            embed = discord.Embed(color = 0xe22f32)
            embed.add_field(name="**Music Playback**", value="Resuming music playback..", inline=True)
            embed.set_footer(text="Kengo System")
            await ctx.send(embed=embed)

    @commands.command()
    async def volume(self, ctx, vol : int):
        server = ctx.guild
        voice_client = server.voice_client
        player = self.client.wavelink.get_player(ctx.guild.id)
        if player.is_playing:

            if int(vol) <= 100:
                x = int(round(int(vol) / int(10)))
                y = int(10) - int(x)
                L = x * u'▰'
                R = y * u'▱'
                vlvl = L + R
                # await ctx.send(L + R)

                embed = discord.Embed(color = 0xe22f32)
                # embed.add_field(name="Volume (old)", value=player.volume, inline=True)
                await player.set_volume(vol)
                # embed.add_field(name="Volume (new)", value=player.volume, inline=True)
                embed.add_field(name="**Volume**", value=vlvl, inline=False)
                embed.set_footer(text="Volume Control")
                await ctx.send(embed=embed)

    @commands.command()
    async def nextup(self, ctx):
        track = queue[0]
        embed = discord.Embed(title="**Playing Music**", description="Coming up next..", color = 0xe22f32)
        embed.add_field(name="***Now Playing***", value="{}".format(queue[0]), inline=True)
        embed.set_thumbnail(url=str(track.thumb))
        embed.set_footer(text="Music Player")
        await ctx.send(embed=embed)

    @commands.command()
    async def playing(self, ctx):
        gicon = ctx.guild.icon_url
        player = self.client.wavelink.get_player(ctx.guild.id)

        current = player.current
        seconds = int(int(current.length) / int(1000))
        minutes = seconds / int(60)
        remains = seconds % int(60)

        print("Song length: {}:{}".format(int(minutes), int(remains)))

        embed = discord.Embed(title="**Playing Music**", description="Currently playing.", color = 0xe22f32)
        embed.add_field(name="***Now Playing***", value="{}".format(player.current.title), inline=True)
        embed.add_field(name="**Song Length**", value="{}:{}".format(int(minutes), int(remains)), inline=True)
        embed.set_thumbnail(url=str(current.thumb))
        embed.set_footer(text="Music Player")
        await ctx.send(embed=embed)

    @commands.command(aliases=["link"])
    async def seek(self, ctx, min : float):
        player = self.client.wavelink.get_player(ctx.guild.id)
        length = player.current.length

        mseconds = int(float(min) * float(60000))

        end = round(float(int(length) / int(60000)), 2)
        per = float(min) / float(end)
        ptg = round(float(per) * int(100), 1)

        if player.is_playing:
            await player.seek(position=mseconds)
            await ctx.send("New player position: {} out of {} minutes".format(float(min), round(player.current.length/60000, 2)))
            await ctx.send("Skipping {}% into the song.".format(ptg))

    @commands.command()
    async def scan(self, ctx, per):
        player = self.client.wavelink.get_player(ctx.guild.id)
        length = player.current.length
        perc = per[:-1]

        ptg = float(perc) / int(100)
        end = round(float(int(length) / int(60000)), 2)
        min = float(ptg) * float(end)

        mseconds = int(float(min) * float(60000))

        if player.is_playing:
            await player.seek(position=mseconds)
            await ctx.send("Skipping {}% into the song.".format(perc))


def setup(client):
    client.add_cog(Music(client))
