# Libraries to make the bot work
import os 
import discord
import random
import asyncio
from discord.ext import commands
import json
import urllib.request


TOKEN = ... 
#Replace token with your own bot's token if you want to reproduce bot results, the token connects the python file to the bot

BOT_PREFIX = ("?", "!") 
client = commands.Bot(command_prefix=BOT_PREFIX)
#the BOT_PREFIX are the prefixes that work with @client.command and the line of code under allows for it to be registered

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='A Variety of Games'))
    print(f'{client.user} has connected to Discord!')    
#the code above are the commands that run when the bot file is run
#the print statements are printed out to the console so the developer can test when the bot is running
#the await client.change ... is what happens within discord(The Bot is shown as active and has a title of "Playing A Variety of Games")


@client.command()
async def helper(ctx):
    message = """Activate a command using ! or ?\n
                 Command list includes:\nhelper\nhello\nping\ngamelist\nplay"""
    await ctx.send(message)
#@client.command is activated using one of the bot prefixes (in this case !helper would be the command)
#this command just tells the user what commands are available
#created a variable for message for formatting concerns
#await ctx.send allows to send the message

@client.command()
async def hello(ctx):
    msg = 'Hello {0.author.mention}! I am GameBot, pleasure to meet you!'.format(ctx)
    await ctx.send(msg)
#this command makes the bot respond back to the user who used !hello with an @

@client.command()
async def ping(ctx):
    latency = client.latency
    await ctx.send(latency)
#the client.latency command is used to see how long it takes for the bot to send a message to the user

@client.command()
async def gamelist(ctx):
    message = '''
    List of games includes:\nCoinGame\nDieGame\nGuessingGame\nMemoryNumGame\nMemoryWordGame\nWordGame2\n 
In order to play, type !play followed by a game name
    '''
    #make word game like 8 ball just various letters and quicker time;also another version have you seen this with a score counter; tic tac toe is also cool
    await ctx.send(message)
#just like the #helper function, using a seperate message in order to format the message

@client.event
async def on_message(message):
    #on_message is when a message is sent, using the value of message
    if message.content.startswith('!play') or message.content.startswith('?play'):
    #just like a prefix command however needs to be analyzed seperately because it is an event with an on_message  
        channel = message.channel 
        #shortcut for sending messages so message.channel does not need to be used every time
        userInput = message.content[6:] 
        #the part of the message after the "!/?play, allowing it to be analyzed for the game type"
        startmessage = 'Initializing ' + userInput + '...' 
        #An initializing message to show the user what game they are playing
        

        if userInput.lower() == "coingame": 
        #no matter the case spelling from the user's message, as long the letters match the following code will run
            await channel.send(startmessage) 
            #if the game name is valid the startmessage is sent
            await channel.send("I will flip a coin, make your guess on what side it lands on:") 
            #telling the user how the game is played
            
            def is_correct(m):
                return m.author == message.author
            #function that confirms that the author who sent the initial message is the one who is answering

            def coinval_convert(coinval):
                if coinval == 0:
                    return "Heads"
                elif coinval == 1:
                    return "Tails"
            #converts an integer value to either Heads or Tails (which the game needs)

            coinval = random.randint(0,1) #a random value generator with two values
            new_coinval = coinval_convert(coinval) #converting the number value into a string (Heads or Tails)
            
            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(new_coinval))
            #the try/except code is for user input, checks for an input of an message and that it is sent by the initial sender, saving it to a variable
            # if the user does not send it before the timeout value, the program will end, returning a message giving the correct answer

            if user_guess.content.lower() == new_coinval.lower():
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(new_coinval))
            #the if/else is to match the user's guess to the value of the coinflip, with the .lower allowing for different capitalization
            
            await channel.send('You had a {:.2%} chance of getting it right!'.format(1/2))
            #displaying the chance the user had to get the answer right

        elif "diegame" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("I will roll a 6 sided die, make your guess on what number it lands on:")
            
            def is_correct(m):
                return m.author == message.author and m.content.isdigit()
            #similar to the code for coin game, the .isdigit() confirms the user input is a digit

            dieval = random.randint(1,6)
            #generates a random dice val

            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 10.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(dieval))

            if user_guess.content == str(dieval):
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(dieval))   
            
            await channel.send('You had a {:.2%} chance of getting it right!'.format(1/6))
            #majority of coingame code was used for diegame code

        elif "guessinggame" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("Type two numbers to set a range for the guessing:")
            
            def is_correct(m):
                return m.author == message.author and m.content.isdigit()
            
            try:
                range1 = await client.wait_for('message', check=is_correct, timeout = 8.0)
                range2 = await client.wait_for('message', check=is_correct, timeout = 8.0)
                range1 = int(range1.content) #converts message content into integer
                range2 = int(range2.content) #converts message content into integer
            except asyncio.TimeoutError:
                range1 = 1
                range2 = 100
                await channel.send("Sorry, you ran out of time. Choose two numbers faster.\nA default from 1 to 100 has been set.")
            #this first try/except in the code has the user set a range for where to guess a number
            # If time runs out for the user's interval, then a default of 1 to 100
            
            numberval = random.randint(range1,range2) # generates a random value given the range
            bottom = (range2-range1)+1 #this value is used for percentage purposes

            await channel.send("Guess a number from " + str(range1) + " to " + str(range2) + " now!")

            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(numberval))
            # the second try/except is for the user's guess

            if user_guess.content == str(numberval):
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(numberval))
            
            await channel.send('You had a {:.2%} chance of getting it right!'.format(1/bottom))
        
        elif "memorynumgame" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("In this game you will have 10 seconds to remember a number. How good is your memory?")
            await channel.send("What level do you want?(Number of Digits)")
            
            def is_correct(m):
                return m.author == message.author and m.content.isdigit()
            
            try:
                level = await client.wait_for('message', check=is_correct, timeout = 8.0)
                level = int(level.content) #converts message into integer
            except asyncio.TimeoutError:
                return await channel.send("Sorry, you ran out of time. Choose a level faster next time.")
                #the return kicks the user out of the program

            range1 = (10 **(level-1)) 
            range2 = (10 ** level)-1
            #doing a bit of math, the range is set so that values only in that digit are present 
            tomemorize = random.randint(range1,range2) # a random value for only that digit value
            await channel.send("Memorize this number before it gets deleted!") 
            botMessage = await channel.send(tomemorize) #stores the message of the number as a variable
            await asyncio.sleep(10) #code makes it so the user has to wait 10 seconds to memorize and no responses can be sent
            await botMessage.delete() #the message is deleted after the 10 seconds so the user does not read it off

            await channel.send("What " + str(level) + " digit number was that?")

            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(tomemorize))

            if user_guess.content == str(tomemorize):
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(tomemorize))

        elif "memorywordgame" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("In this game you will have 1 second to remember a random word. How good is your memory?")
            
            def is_correct(m):
                return m.author == message.author and type(m.content) == str

            #takes a list of words from url and turns it into a variable
            url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
            words = json.loads(url.read())
            tomemorize = random.choice(words)
            await channel.send("Memorize this word before it gets deleted!") 
            botMessage = await channel.send(tomemorize) #stores the message of the word as a variable
            await asyncio.sleep(1) #code makes it so the user has to wait 1 seconds to memorize and no responses can be sent
            await botMessage.delete() #the message is deleted after the 1 seconds so the user does not read it off

            await channel.send("What word was that?")

            try:
                user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
            except asyncio.TimeoutError:
                 return await channel.send('Sorry, you ran out of time. The answer was {}.'.format(tomemorize))

            if user_guess.content == tomemorize:
                await channel.send('Yay, you answered correct!')
            else:
                await channel.send('WRONG!! It was actually {}.'.format(tomemorize))
      
        elif "wordgame2" == userInput.lower():
            await channel.send(startmessage)
            await channel.send("In this game you will have 3 seconds to determine if you have seen the word before.")
            await channel.send("Three strikes and you're out!")
            
            #determines if the new message is sent by the same as the initial !play message
            def is_correct(m):
                return m.author == message.author and type(m.content) == str

            def yesno_convert(answer):
                if answer.lower() == "yes":
                    return True
                elif answer.lower() == "no":
                    return False
            #converts an yes or no string value to either True or False

            #takes a list of words from url and turns it into a variable
            url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
            words = json.loads(url.read())
            tomemorize = random.choice(words) 
            botMessage = await channel.send("Look at the first word before it gets deleted: " + tomemorize) #stores the message of the word as a variable
            await asyncio.sleep(3) #code makes it so the user has to wait 3 seconds to memorize and no responses can be sent
            await botMessage.delete() #the message is deleted after the 3 seconds so the user does not read it off
            wordlist = []
            wordlist.append(tomemorize)

            await channel.send("The game has started!") 
            strikes = 3
            points = 0
            #creates a while loop so continues until gameends
            while strikes > 0:
                length = len(wordlist)
                randnumber = random.randint(1,5)
                #generates a random int val
                
                if length < 4:
                    tomemorize = random.choice(words)
                elif randnumber == 4 or randnumber == 5:
                    randval = random.randint(0,length-1)
                    tomemorize = wordlist[randval]
                else:
                    tomemorize = random.choice(words)
                
                botMessage = await channel.send("3 seconds to determine... " + tomemorize) #stores the message of the word as a variable
                await asyncio.sleep(3) #code makes it so the user has to wait 3 seconds to memorize and no responses can be sent
                await botMessage.delete() #the message is deleted after the 3 seconds so the user does not read it off
                
                await channel.send("Has the word been shown before?") 

                try:
                    user_guess = await client.wait_for('message', check=is_correct, timeout = 8.0)
                except asyncio.TimeoutError:
                    await channel.send('Sorry, you ran out of time.')
                    break #if no answer in 8 seconds, program breaks out of while loop, displays score, and ends

                #uses the function to convert yes or no to true or false
                useranswer = yesno_convert(user_guess.content)
                if tomemorize in wordlist and useranswer:
                    points = points + 1
                    await channel.send('Correct!\nStrikes left: ' + str(strikes) + "\nPoints: " + str(points))
                elif tomemorize not in wordlist and not useranswer:
                    wordlist.append(tomemorize)
                    points = points + 1
                    await channel.send('Correct!\nStrikes left: ' + str(strikes) + "\nPoints: " + str(points))
                else:
                    strikes = strikes - 1
                    await channel.send('WRONG!!\nStrikes left: ' + str(strikes) + "\nPoints: " + str(points))

            await channel.send('Game Over. You scored ' + str(points) + ' points.')
            
        else:
            await channel.send("Please choose a valid game name from gamelist")
        #else if no valid game is put after the !/?play (or if empty), then bot responds by saying it was not a valid game 

            
    await client.process_commands(message) 
    #if an on_message event is not being run, the file will process it anyways so other commands outside of the on_message can be run


client.run(TOKEN)
#this is the command that finally runs the bot using the token value