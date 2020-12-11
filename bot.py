import discord, asyncio, random, glob, os, threading

from pymongo import MongoClient
from asyncio import sleep
from discord.ext import commands, tasks
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime

# Using cogs for organization of bot (so this isn't a 500 line python script).
# The more finicky functions are kept in this main script as I don't want to add more complexity on top of them.

# Anything here is run before ```bot.run(str(token.readline()))``` is run, so you cannot access anything the bot usually can. 
# If you want a channel or member object, you need to wait for on_ready() to be called or request it in on_ready()

# Additionally, it is worth noting that everything pushed to Heroku is reverted to the state is was when pushed every 24 hours, making
# persistent storage very annoying to deal with

# For splitting the bot up
initial_extensions = ['cogs.roles','cogs.games','cogs.util']

# General Setup
bot = commands.Bot(command_prefix=("sudo ", "Sudo ", "SUDO ", "sudo"))
bot.remove_command("help")
embed_colour = discord.Colour.red()

# Pain related Setup. I know the mongoDB password is just sitting there but like... the data is literally how many times we've typed "pain" so idc lole
random.seed()
cluster = MongoClient("mongodb+srv://fizz:fizz2020@cluster0.vl4ko.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["pain"]
pain = []

# Channel for storing the pain logs
counting_room_id = 755275676311093369
# Dictionary with date and time as key, with paincount as value
joy_list = ["JOY", "BLESSED", "COMFORT", "HAPPY", "RELIEF", "WELLNESS", "POG"]

# Function that runs when the bot is fully ready (can access the cache)
@bot.event
async def on_ready():
    
    global counting_room
    counting_room = bot.get_channel(counting_room_id)
    start_room = bot.get_channel(758412054125346826)
    await start_room.send("Started :D")

    for extension in initial_extensions:
        bot.load_extension(extension)

    # Finding what pain was sent last and adding it to pain_list, which should be empty
    try:
        last_pain = await counting_room.fetch_message(counting_room.last_message_id)
        pain.append(int(last_pain.content))
    except:
        print("uh oh")

    # Start new thread to run a timer
    thread = threading.Thread(target = await checkTime())
    thread.start()
    thread.join()

    print("bot.py: Extensions loaded, Pain {} - Bot Ready".format(int(last_pain.content)))

# All functionality that checks every sent message.
@bot.event
async def on_message(message):
    
    await bot.process_commands(message)

    if message.content.upper() == "FUCK":
        await message.channel.send(file=discord.File(open("media/fuck.mp4", "rb")))

    if message.content.upper() == "SOBBING":
        await message.channel.send(file=discord.File(open("media/sobbing.png", "rb")))

    if message.content.upper() == "PAIN" or message.content.upper() == "CHAIN" or message.content == '🍞' or message.content == '🥖' or message.content.upper() == "PAIN PEKO":
        await pain_message(message)

    if message.content.upper() in joy_list:
        await joy_message(message)

async def pain_message(message):
    # Looks at last value in pain_list, adds 1 pain, and adds to the list.

        # Updating pain and sending to mongoDB
        new_pain = pain[-1] + 1
        pain.append(new_pain)
        collection.insert_one({"pain": new_pain, "time": datetime.now().strftime("%H:%M:%S"), "user_id": message.author.id})

        # Choosing random image from folder
        pain_folder = len(glob.glob("pain/*"))
        pain_pic = random.uniform(0, pain_folder - 1)

        # Writing pain on it
        img = Image.open("pain/{}.png".format(int(pain_pic)))
        W, H = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("media/helvetica.ttf", int(H / 7))
        
        if new_pain >= 0:
            text = "pain: {}".format(new_pain)
        else:
            text = "joy: {}".format(abs(new_pain))
            
        w, h = draw.textsize(text, font=font)
        # Drawing text in middle and adding border
        draw.text(((W-w)/2,(H-h)/2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+2,(H-h)/2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2,(H-h)/2+2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+2,(H-h)/2+2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+1,(H-h)/2+1), text, (255, 255, 255), font=font)
        img.save("pain/temp.png")

        if (new_pain % 10 == 0):
            await counting_room.send(pain[-1])
            
        if (new_pain % 100 == 0): 
            await message.channel.send(file=discord.File(open("media/pain.mp4", "rb")))

        await message.channel.send(file=discord.File(open("pain/temp.png", "rb")))

async def joy_message(message):
        # Looks at last value in pain_list, adds 1 pain, and adds to the list.

        # Updating pain and sending to mongoDB 
        new_pain = pain[-1] - 1
        pain.append(new_pain)
        collection.insert_one({"pain": new_pain, "time": datetime.now().strftime("%H:%M:%S"), "user_id": message.author.id})

        # Choosing random image from folder
        pain_folder = len(glob.glob("joy/*"))
        pain_pic = random.uniform(0, pain_folder - 1)

        # Writing joy on it
        img = Image.open("joy/{}.png".format(int(pain_pic)))
        W, H = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("media/helvetica.ttf", int(H / 7))

        if new_pain >= 0:
            text = "pain: {}".format(new_pain)
        else:
            text = "joy: {}".format(abs(new_pain))

        w, h = draw.textsize(text, font=font)
        # Drawing text in middle and adding border
        draw.text(((W-w)/2,(H-h)/2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+2,(H-h)/2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2,(H-h)/2+2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+2,(H-h)/2+2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+1,(H-h)/2+1), text, (255, 255, 255), font=font)
        img.save("joy/temp.png")

        if (new_pain % 10 == 0):
            await counting_room.send(pain[-1])

        if (new_pain % 100 == 0): 
            await message.channel.send(file=discord.File(open("media/pain.mp4", "rb")))

        await message.channel.send(file=discord.File(open("joy/temp.png", "rb")))

    
# TODO Update this
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        description="Ṭ̶̔ḩ̴̦̑͗͜e̶̦͛r̷̮̹̂ͅe̸̬͖͊͂ ̷̖̭̻̃̐ì̸̛̲̥͗ș̸̆ ̸͇̅n̵̢͓͚͗͛ǫ̴̣̅ ̸̘̌͆̑ḫ̶̫̰̑e̷̼̼̒l̸̲͍̯̈́͂͊p̵̋̂͋͜",
        colour=embed_colour,
    )
    await ctx.message.channel.send(embed=embed)

# TODO Switch this to reading stuff off a .csv or something
# Dictionary of textbooks/guides related to course
subjects = {
    "ENPH": "270 - http://93.174.95.29/main/CE1E90DC739863A9788F6324038E2DFB\nThe Bible - http://93.174.95.29/main/05D120938A4D7EBB5A706CE17F66B547",
    "MECH": "260/360 - http://93.174.95.29/main/4B6F6F6DF336EF7DB2219A8E66B1C498\n325 - Mott: http://library.lol/main/3BE591092F39D20F7F6A1ECFEF90A6CA - Shigley:",
    "ELEC": "nothing here yet, but MNA >> Mesh",
    "PHYS": "250 - http://93.174.95.29/main/318C1507190566EA13AEB003893A7569\n",
    "MATH": "217 - http://www.math.ubc.ca/~CLP/CLP3/ & http://www.math.ubc.ca/~CLP/CLP4/\n255/257 - https://www.jirka.org/diffyqs/diffyqs.pdf\n",
    "CPEN": "https://stackoverflow.com/",
    "APSC": "https://mech2.sites.olt.ubc.ca/files/2014/12/S01_6161.jpg",
    "SPECS": "https://docs.google.com/spreadsheets/d/119mEbyerER02r8lSYzcT4sovFmxW48su0XgUqfFStf0/edit?usp=sharing",
}

# Allows users to get saved
@bot.command()
async def get(ctx):
    request = ctx.message.content.upper()

    if "SPECS" in request:
        embed = discord.Embed(
            title="Robot Summer component datasheets (WIP):",
            description=subjects["SPECS"],
            colour=embed_colour,
        )
        await ctx.message.channel.send(embed=embed)

    elif "ALL" in request:
        for subject in subjects:
            await ctx.message.channel.send("**{} Textbooks:**".format(subject))
            await ctx.message.channel.send(subjects[subject])

    else:
        for subject in subjects:
            if subject in request:
                embed = discord.Embed(
                    title="{} Textbooks:".format(subject),
                    description=subjects[subject],
                    colour=embed_colour,
                )
                await ctx.message.channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    # Sends new members a private message reminding them to assign themselves a role

    embed = discord.Embed(
        description="**Welcome to the Fizz Discord <@{}>!**\n\nAssign yourself a role by heading to #role-assignment".format(
            member.id
        ),
        colour=embed_colour,
    )
    await member.send(embed=embed)

@bot.command()
async def iskevinbald(ctx):
    # Essential command, do not remove

    embed = discord.Embed(description="Yes", colour=embed_colour)
    await ctx.message.channel.send(embed=embed)

async def checkTime():
    # Checking every second to see if it is 11:59:50, at which point the bot saves the day's pain and posts it in a server, 
    # as a way to persist through Heroku's daily restart. Hidden at bottom of script so no one seems my while loop
    print("Timer Started")

    while(True):
        current_time = datetime.now().strftime("%H:%M:%S")
        #print(current_time)

        if(current_time == '07:59:55'):
            # Send pain value so the bot can read it on refresh
            await counting_room.send(pain[-1])
        
        await sleep(1)

# Rudimentary token security measure. If it leaks I must have done something very wrong
token = open("token.txt", "r")
bot.run(str(token.readline()))
token.close()
