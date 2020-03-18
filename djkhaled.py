import discord
import youtube_dl

from discord.ext import commands

TOKEN = 'Njg5ODQ4NTc3Njc3MDY2MjQx.XnI12w.DVwjw-1TYwNEXSS6VNUmNZrmgOs'
client = commands.Bot(command_prefix = '.')

palyers = {}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("another one"))
    print("DJ Khaled!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I cannot find that command bruh")

@client.command()
async def ping(ctx):
    await ctx.send(f"Could be purple, it could be ping. {round(client.latency * 1000)}ms")

@client.command()
async def shout(ctx):
    await ctx.send("DJ Khaled!")

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

client.run(TOKEN)