import discord, asyncio, random, glob, os, threading, argparse, sys, time

from pymongo import MongoClient
from asyncio import sleep
from discord.ext import commands, tasks
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime

# Using cogs for organization of bot (so this isn't a 500 line python script).
# The more finicky functions are kept in this main script as I don't want to add more complexity on top of them.

# Anything here is run before ```bot.run(str(token.readline()))``` is run, so you cannot access anything the bot usually can.
# If you want a channel or member object, you need to wait for on_ready() to be called or request it in on_ready()

# This regression of code won't work for Heroku, for reasons you'd understand if you've used Heroku to host a bot.

# For splitting the bot up
initial_extensions = ["cogs.roles", "cogs.games", "cogs.util"]

# General Setup
bot = commands.Bot(command_prefix=("sudo ", "Sudo ", "SUDO ", "sudo"))
bot.remove_command("help")
embed_colour = discord.Colour.red()

# Pain related Setup. I know the mongoDB password is just sitting there but like... the data is literally how many times we've typed "pain" so idc lol
random.seed()
cluster = MongoClient(
    "mongodb+srv://fizz:fizz2020@cluster0.vl4ko.mongodb.net/<dbname>?retryWrites=true&w=majority"
)
db = cluster["discord"]
collection = db["paincount"]

# Pain
pain_queue_running = False
order = 0
queue = {}

# Trigger words for pain/joy
pain_list = ["PAIN", "AGONY", "SUFFERING", "DESPAIR", "CHAIN", "🍞", "🥖", "PAIN PEKO"]
joy_list = ["JOY", "BLESSED", "COMFORT", "HAPPY", "RELIEF", "WELLNESS", "POG"]

# Gets the most recent pain entry, just for initialization
pain = list(collection.find().sort("time",-1).limit(1))[0]["pain"]

# Function that runs when the bot is fully ready (can access the cache)
@bot.event
async def on_ready():

    # Load the cogs
    for extension in initial_extensions:
        bot.load_extension(extension)

    print("bot.py: Extensions loaded, Bot Ready")


# All functionality that checks every sent message.
@bot.event
async def on_message(message):

    global pain_queue_running
    # Allows other message based stuff to work
    await bot.process_commands(message)

    if message.content.upper() == "FUCK":
        await message.channel.send(file=discord.File(open("media/fuck.mp4", "rb")))

    if message.content.upper() == "SOBBING":
        await message.channel.send(file=discord.File(open("media/sobbing.png", "rb")))

    if message.content.upper() in pain_list:
        # creates a new pain image
        await pain_message(message)
        # start thread that sends pain on a delay
        if not pain_queue_running:
            pain_queue_running = True
            await pain_queue()

    if message.content.upper() in joy_list:
        # same
        await joy_message(message)
        if not pain_queue_running:
            pain_queue_running = True
            await pain_queue()


async def pain_message(message):

    # Updating pain and sending to mongoDB
    global pain
    global order
    global queue

    pain += 1
    order += 1
    queue[order] = message.channel

    date = int(time.time())
    collection.insert_one({"pain": pain, "time": date, "user_id": message.author.id})

    # Choosing random image from folder
    pain_folder = len(glob.glob("media/pain/*"))
    pain_pic = random.uniform(0, pain_folder)

    # Writing pain on it
    img = Image.open("media/pain/{}.png".format(int(pain_pic)))
    W, H = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("media/helvetica.ttf", int(H / 7))

    if pain >= 0:
        text = "pain: {}".format(pain)
    else:
        text = "joy: {}".format(abs(pain))

    w, h = draw.textsize(text, font=font)
    # Drawing text in middle and adding border
    draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2 + 2, (H - h) / 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2, (H - h) / 2 + 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2 + 2, (H - h) / 2 + 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2 + 1, (H - h) / 2 + 1), text, (255, 255, 255), font=font)
    img.save(f"media/queue/{order}.png")

    if pain % 100 == 0:
        await message.channel.send(file=discord.File(open("media/pain.mp4", "rb")))

    # await message.channel.send(file=discord.File(open("pain/temp.png", "rb")))


async def joy_message(message):

    # Updating pain and sending to mongoDB
    global pain
    global order
    global queue

    pain -= 1
    order += 1
    queue[order] = message.channel

    date = int(time.time())
    collection.insert_one({"pain": pain, "time": date, "user_id": message.author.id})

    # Choosing random image from folder
    pain_folder = len(glob.glob("media/joy/*"))
    pain_pic = random.uniform(0, pain_folder)

    # Writing joy on it
    img = Image.open("media/joy/{}.png".format(int(pain_pic)))
    W, H = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("media/helvetica.ttf", int(H / 7))

    if pain >= 0:
        text = "pain: {}".format(pain)
    else:
        text = "joy: {}".format(abs(pain))

    w, h = draw.textsize(text, font=font)
    draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2 + 2, (H - h) / 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2, (H - h) / 2 + 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2 + 2, (H - h) / 2 + 2), text, font=font, fill=(0, 0, 0))
    draw.text(((W - w) / 2 + 1, (H - h) / 2 + 1), text, (255, 255, 255), font=font)
    img.save(f"media/queue/{order}.png")

    if pain % 100 == 0:
        await message.channel.send(file=discord.File(open("media/pain.mp4", "rb")))


async def pain_queue():

    global pain_queue_running
    global queue

    while len(queue) > 0:

        oldest = min(queue.keys())

        # post and remove the picture
        with open(f"media/queue/{oldest}.png", "rb") as painfile:
            await queue[oldest].send(file=discord.File(painfile))

        del queue[oldest]
        os.remove(f"media/queue/{oldest}.png")
        time.sleep(1)

    pain_queue_running = False


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


@bot.command(brief="Checks if Kevin Lin is bald")
async def iskevinbald(ctx):
    # Essential command, do not remove

    embed = discord.Embed(description="Yes", colour=embed_colour)
    await ctx.message.channel.send(embed=embed)


# quick parser to make development a bit easier
def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=bool, default=False, help="there is no help")

    return parser

@bot.command(brief="Admin/Development Command")
async def force_quit(ctx):
    if ctx.message.author.id == 168388106049814528:
        with open("pain.txt", "w") as painfile:
            painfile.write(str(pain))
            exit()


def main():
    args = build_argparser().parse_args()

    # Rudimentary token security measure. If it leaks I must have done something very wrong
    if args.dev:
        token = open("devtoken.txt", "r")
    else:
        token = "NzA3NDk0Mzk5NjA4NzUwMTIx.XrJngQ.XDtq_tmYQ34JxFixjW1R8QPMoBg"

    bot.run(str(token.readline()))
    token.close()


if __name__ == "__main__":
    sys.exit(main() or 0)
