# Work with Python 3.6
import os
import discord
import random
import asyncio
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
                 Command list includes:\nhelper\nhello\nping\ngamelist\nplay"""
    await ctx.send(message)

@client.command()
async def hello(ctx):
    msg = 'Hello {0.author.mention}'.format(ctx)
    await ctx.send(msg)

@client.command()
async def ping(ctx):
    latency = client.latency
    await ctx.send(latency)

@client.command()
async def gamelist(ctx):
    message = '''
    List of games includes:\nCoinGame\nDieGame\nRememberTheNumber\nGuessMyNumber\n
In order to play, type !play followed by a game name
    '''
    await ctx.send(message)

@client.event
async def on_message(message):
    if message.content.startswith('!play') or message.content.startswith('?play'):
        channel = message.channel
        userInput = message.content[6:]
        startmessage = 'Initializing ' + userInput + '...'
        

        if userInput.lower() == "coingame":
            await channel.send(startmessage)
            await channel.send("I will flip a coin, make your guess on what side it lands on:")
            
            def is_correct(m):
                return m.author == message.author
            
            def coinval_convert(coinval):
                if coinval == 0:
                    return "Heads"
                elif coinval == 1:
                    return "Tails"

            coinval = random.randint(0,1)
            new_coinval = coinval_convert(coinval)
            
            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(new_coinval))

            if user_guess.content.lower() == new_coinval.lower():
                await channel.send('Yay, you answered right! You had a {:.2%} chance of getting it right!'.format(1/2))
            else:
                await channel.send('WRONG!! It was actually {}.'.format(new_coinval))
    
        elif "diegame" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("I will roll a die, make your guess on what number it lands on:")
            
            def is_correct(m):
                return m.author == message.author and m.content.isdigit()
            
            dieval = random.randint(1,6)
            print(dieval)
            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 10.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(dieval))

            if user_guess.content == str(dieval):
                await channel.send('Yay, you answered right! You had a {:.2%} chance of getting it right!'.format(1/6))
            else:
                await channel.send('WRONG!! It was actually {}.'.format(dieval))

        elif "guessmynumber" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("Type two numbers to set a range for the guessing, :")
            
            def is_correct(m):
                return m.author == message.author and m.content.isdigit()
            
            try:
                range1 = await client.wait_for('message', check=is_correct, timeout = 8.0)
                range2 = await client.wait_for('message', check=is_correct, timeout = 8.0)

            except asyncio.TimeoutError:
                range1 = 1
                range2 = 100
                return await channel.send("Sorry, you ran out of time. Choose two numbers faster. \nA default from 0 to 100 has been set.")
                
            numberval = random.randint(range1,range2)
            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(numberval))

            if user_guess.content == str(dieval):
                await channel.send('Yay, you answered right!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(numberval))
        else:
            await channel.send("Please choose a valid game name from gamelist")
        
  
    await client.process_commands(message)    

"""
@client.command()
async def play(ctx, *args):
    if not args:
        await ctx.send("Please add the game name you would like to play")
    else:
        startmessage = 'Initializing ' + args[0] + '...'
        if args[0] == 'CoinGame':
            await ctx.send(startmessage)
            await ctx.send("I will flip a coin, make your guess on what side it lands on:")
            
            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()
            
            def coinval_convert(coinval):
                if coinval == 0:
                    coinval == "Heads"
                elif coinval == 1:
                    coinval == "Tails"
                return coinval

            coinval = random.randint(0,1)
            coinval = coinval_convert(coinval)
            
            #try:
            user_guess = await client.wait_for('message', check=is_correct)
            # except asyncio.TimeoutError:
            #     return await ctx.send('Sorry, you took too long it was {}.'.format(coinval))

            if user_guess.content == coinval:
                await ctx.send('You are right!')
            else:
                await ctx.send('Oops. It is actually {}.'.format(coinval))
"""
        

# @client.event
# async def on_message(message):
#     if message == 'CoinGame':
#         coinval = random.randint(0,1)
#         print(coinval)


    # if client.user.id != message.author.id:
    #     if 'foo' in message.content:
    #         await client.send_message(message.channel, 'bar')

    # await client.process_commands(message)

# @client.command()
# async def stock(ctx, *args):
#     if not args:
#         await ctx.send("Please add a stock ticker")
#     else:
#         await ctx.send(args[0])

client.run(TOKEN)