# Work with Python 3.6
import os
import discord

from discord.ext import commands

TOKEN = 'NzM4NjAyNTMyMTUwMDUwODg2.XyOTNg.DCgkv0bX4cFb6ip31Ba9W5_DAIY'

BOT_PREFIX = ("?", "!")
client = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='Stock bot in testing!'))
    print(f'{client.user} has connected to Discord!')

@client.command
async def help(ctx):
    message = """Activate a command using ! or ?\n\n 
                 Command list includes: \n help \n hello \n gamechoices \n ping"""
    await ctx.send(message)

#@client.event(name='gamechoices')
#async def 


@client.command()
async def ping(ctx):
    latency = client.latency
    await ctx.send(latency)

@client.command()
async def hello(ctx):
    msg = 'Hello {0.author.mention}'.format(message)
    await ctx.send(msg)

# @client.command()
# async def stock(ctx, *args):
#     if not args:
#         await ctx.send("Please add a stock ticker")
#     else:
#         await ctx.send(args[0])


# @client.event
# async def on_message(message):
#     # we do not want the bot to reply to itself
#     if message.author == client.user:
#         return
    
#     if message.content.startswith('!hello'):
#         msg = 'Hello {0.author.mention}'.format(message)
#         await message.channel.send(msg)

client.run(TOKEN)