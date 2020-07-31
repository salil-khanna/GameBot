# Work with Python 3.6
import os
import discord
import random
import asyncio
from discord.ext import commands

TOKEN = 'NzM4NjAyNTMyMTUwMDUwODg2.XyOTNg.dSFYt7rKAqx8AznF2FT418nxmgE'

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
    List of games includes:\nCoinGame\nDieGame\nGuessTheNumber\nRememberheNumber(Currently not working)\n
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
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(new_coinval))
            
            await channel.send('You had a {:.2%} chance of getting it right!'.format(1/2))

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
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(dieval))   
            
            await channel.send('You had a {:.2%} chance of getting it right!'.format(1/6))

        elif "guessthenumber" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("Type two numbers to set a range for the guessing:")
            
            def is_correct(m):
                return m.author == message.author and m.content.isdigit()
            
            try:
                range1 = await client.wait_for('message', check=is_correct, timeout = 8.0)
                range2 = await client.wait_for('message', check=is_correct, timeout = 8.0)
                range1 = int(range1.content)
                range2 = int(range2.content)

            except asyncio.TimeoutError:
                range1 = 1
                range2 = 100
                await channel.send("Sorry, you ran out of time. Choose two numbers faster.\nA default from 1 to 100 has been set.")

            
            numberval = random.randint(range1,range2)
            print(numberval)
            bottom = (range2-range1)+1

            await channel.send("Guess a number from " + str(range1) + " to " + str(range2) + " now!")

            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(numberval))

            if user_guess.content == str(numberval):
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(numberval))
            
            await channel.send('You had a {:.2%} chance of getting it right!'.format(1/bottom))

        else:
            await channel.send("Please choose a valid game name from gamelist")
            
  
    await client.process_commands(message)    

# @client.command()
# async def stock(ctx, *args):
#     if not args:
#         await ctx.send("Please add a stock ticker")
#     else:
#         await ctx.send(args[0])

client.run(TOKEN)