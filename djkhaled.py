import discord
import youtube_dl
import os
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system

from discord.ext import commands

queuelist = []

TOKEN = 'Njg5ODQ4NTc3Njc3MDY2MjQx.XnbV2g.lQp6g3-adZVY5e2exUsKxruEMYw'
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("another one"))
    print("DJ Khaled is ready!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I cannot find that command bruh")

@client.command(brief="Check yo ping!")
async def ping(ctx):
    await ctx.send(f"Could be purple, it could be ping. {round(client.latency * 1000)}ms")

@client.command(brief="Shout DJ Khaled!")
async def shout(ctx):
    await ctx.send("DJ Khaled!")

@client.command(pass_context=True, brief="Makes DJ Khaled join your channel")
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("I wanted to put that before, but there's no connection to a channel.")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"I gotta join! Joined '{channel}' channel")

@client.command(pass_context=True, brief="Makes DJ Khaled leave your channel", aliases=['quit'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send("Got a valet, gotta leave...")
    else:
        await ctx.send("Don't think I am the one in a voice channel")

@client.command(pass_context=True, brief="Makes DJ Khaled play a song .play [url]")
async def play(ctx, url: str):
    #queue? make a list!
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except Exception:
        await ctx.send("something's fucked")
        return
    await ctx.send("I don't play about my paper! Playing: " + url)
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()

@client.command(pass_context=True, brief="Change volume")
async def volume(ctx, volume):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.volume = volume
    await ctx.send("Changing it up! Volume: " + volume)

client.run(TOKEN)