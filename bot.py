import discord, asyncio, random, glob, os
from asyncio import sleep
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

# Using cogs for organization of bot (so this isn't a 500 line python script).
# The more finicky functions are kept in this main script as 
initial_extensions = ['cogs.roles','cogs.games','cogs.util']

# Setup
bot = commands.Bot(command_prefix=("sudo ", "Sudo ", "SUDO ", "sudo"))
bot.remove_command("help")
embed_colour = discord.Colour.red()
random.seed()
counting_room_id = 755275676311093369

# Function that runs when the bot is fully ready (can access the cache)
@bot.event
async def on_ready():
    
    global counting_room
    counting_room = bot.get_channel(counting_room_id)

    for extension in initial_extensions:
        bot.load_extension(extension)
    print("bot.py: Extensions loaded - Bot Ready")

# All functionality that checks every sent message.
@bot.event
async def on_message(message):
    
    await bot.process_commands(message)

    if message.content.upper() == "FUCK":
        await message.channel.send(file=discord.File(open("media/fuck.mp4", "rb")))

    if message.content.upper() == "SOBBING":
        await message.channel.send(file=discord.File(open("media/sobbing.png", "rb")))

    if message.content.upper() == "PAIN":
        await pain(message)


async def pain(message):
    # Super hacky way of saving a single number persistenly
        # Reads the most recent message from a certain channel to get the pain index
        # Does basic image processing to a random pain image and saves it as a temporary file 
        # Please don't judge me for this
        try:
            last_message = await counting_room.fetch_message(counting_room.last_message_id)
        except:
            await message.channel.send("something really bad has happened, contact Andrew oh god oh fuck")
            return 
            
        paincount = int(last_message.content)
        
        if paincount % 10 == 0:
            await message.channel.send(file=discord.File(open("pain/main.mp4", "rb")))
            
        paincount += 1
        await counting_room.send(paincount)

        pain_size = len(glob.glob("pain/*"))
        pain = random.uniform(0, pain_size - 1)

        img = Image.open("pain/{}.png".format(int(pain)))
        W, H = img.size
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("media/helvetica.ttf", int(H / 7))
        text = "pain: {}".format(paincount)
        w, h = draw.textsize(text, font=font)
        # Drawing text in middle and adding border
        draw.text(((W-w)/2,(H-h)/2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+2,(H-h)/2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2,(H-h)/2+2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+2,(H-h)/2+2), text, font=font, fill=(0, 0, 0))
        draw.text(((W-w)/2+1,(H-h)/2+1), text, (255, 255, 255), font=font)
        img.save("pain/temp.png")

        await message.channel.send(file=discord.File(open("pain/temp.png", "rb")))

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


# Rudimentary token security measure. If it leaks I must have done something very wrong
token = open("token.txt", "r")
bot.run(str(token.readline()))
token.close()

