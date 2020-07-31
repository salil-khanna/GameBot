# Work with Python 3.6
import os
import discord

from discord.ext import commands

TOKEN = 'NzM4NjAyNTMyMTUwMDUwODg2.XyOTNg.DCgkv0bX4cFb6ip31Ba9W5_DAIY'

BOT_PREFIX = ("?", "!")
client = commands.Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='A Variety of Games'))
    print(f'{client.user} has connected to Discord!')

@client.command()
async def helper(ctx):
    message = """Activate a command using ! or ?\n
                 Command list includes:\nhelper\nhello\ngamelist\nping\nstartgame"""
    await ctx.send(message)

@client.command()
async def gamelist(ctx):
    message = """List of games includes:\nCoinGame\nDiceGame\nRememberTheNumber\nGuessMyNumber"""
    await ctx.send(message)

@client.command()
async def ping(ctx):
    latency = client.latency
    await ctx.send(latency)

@client.command()
async def hello(ctx):
    msg = 'Hello {0.author.mention}'.format(ctx)
    await ctx.send(msg)

# @client.command()
# async def stock(ctx, *args):
#     if not args:
#         await ctx.send("Please add a stock ticker")
#     else:
#         await ctx.send(args[0])

client.run(TOKEN)