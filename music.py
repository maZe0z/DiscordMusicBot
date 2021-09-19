import discord
import requests
from discord import FFmpegPCMAudio
from discord.ext import commands
import youtube_dl


def search(query):
    with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
        try:
            requests.get(query[0])
        except:
            non_url_query = ' '.join(query)
            info = ydl.extract_info(f"ytsearch:{non_url_query}", download=False)['entries'][0]
        else:
            info = ydl.extract_info(query[0], download=False)
    return info, info['formats'][0]['url']


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send('Skipped')
        elif not ctx.voice_client:
            await ctx.send('Nothing to skip')
        else:
            await ctx.send('Unhandled skip function error')

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You aren\'t in a voice channel!')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def play(self, ctx, *args):
        if ctx.author.voice is None:
            return await ctx.send('You aren\'t in a voice channel!')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.disconnect()
            await voice_channel.connect()

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        vc = ctx.voice_client
        video, source = search(args)

        vc.play(FFmpegPCMAudio(source, **FFMPEG_OPTIONS), after=lambda e: print('done', e))
        vc.is_playing()


    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Paused⏸️")

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Resume▶")


def setup(client):
    client.add_cog(Music(client))
