import discord
import asyncio
from asyncio import sleep
from discord.ext import commands

bot = commands.Bot(command_prefix=('sudo ', 'Sudo ', 'SUDO ', 'sudo'))
bot.remove_command('help')
embed_colour = discord.Colour.red()

# TODO: Have bot automatically find these based on the server the command is called
id1 = 709974781252075640
id2 = 709974744329486346
access_role = 689296629836415022

gagged = []

@bot.event
async def on_ready():
	print("Running")

# Basic Utility 

@bot.command()
async def s(ctx):
	
	monkey = bot.get_channel(id1)
	zone = bot.get_channel(id2)
	target = ctx.message.mentions[0]
	ids = (role.id for role in target.roles)

	if ctx.message.mention_everyone or access_role not in ids or not target.voice.self_deaf:
		pass

	else:

		original_channel = target.voice.channel
		await target.send("Wake up <@{}> >:(".format(target.id))
	
		for x in range(4):
			# Moves user back and fourth, muting/deafening each loop
			await target.edit(voice_channel=monkey, deafen=True, mute=True)
			await sleep(0.2)
			await target.edit(voice_channel=zone, deafen=False, mute=False)

		await target.edit(voice_channel=original_channel)

@bot.command()
async def shake(ctx):
	
	monkey = bot.get_channel(id1)
	zone = bot.get_channel(id2)

	target = ctx.message.mentions[0]

	ids = (role.id for role in target.roles)

	if ctx.message.mention_everyone or access_role not in ids or not target.voice.self_deaf:
		pass

	else:

		#current_channel = message.channel
		original_channel = target.voice.channel
		await target.send("Wake up <@{}> >:(".format(target.id))
	
		for x in range(4):

			# Moves user back and fourth, muting/deafening each loop
			await target.edit(voice_channel=monkey, deafen=True, mute=True)
			await sleep(0.2)
			await target.edit(voice_channel=zone, deafen=False, mute=False)

		await target.edit(voice_channel=original_channel)

@bot.command()
async def airstrike(ctx):
	
	monkey = bot.get_channel(id1)
	zone = bot.get_channel(id2)

	target = ctx.message.mentions[0]

	ids = (role.id for role in target.roles)

	if ctx.message.mention_everyone or access_role not in ids or not target.voice.self_deaf:
		pass

	else:

		#current_channel = message.channel
		original_channel = target.voice.channel
	
		for x in range(4):
			await target.send("Wake up <@{}> >:(".format(target.id), file=discord.File(open("blast.jpg", "rb")))
			await target.move_to(channel=monkey)
			await target.move_to(channel=zone)

		await target.move_to(channel=original_channel)

@bot.command()
async def gag(ctx):

	ids = (role.id for role in ctx.message.mentions[0].roles)
	target = ctx.message.mentions[0]

	if ctx.message.mention_everyone or access_role not in ids or ctx.message.author.id in gagged:
			pass

	else:
		if target.id in gagged:
			await ctx.message.channel.send("{} is already muted.".format(target.display_name))
		else:
			gagged.append(target.id)
			await ctx.message.channel.send("Muted {}.".format(target.display_name))

@bot.command()
async def ungag(ctx):

	ids = (role.id for role in ctx.message.mentions[0].roles)
	target = ctx.message.mentions[0]

	if ctx.message.mention_everyone or access_role not in ids or ctx.message.author.id in gagged:
			pass

	else:
		if target.id in gagged:
			gagged.remove(target.id)
			await ctx.message.channel.send("Unmuted {}.".format(target.display_name))
		else:
			await ctx.message.channel.send("{} isn't muted dumbass.".format(target.display_name))

@bot.event
async def on_message(message):
	if message.author.id in gagged:
		await message.delete()
	await bot.process_commands(message)

	if message.content.upper() == "FUCK":
		await message.channel.send(file=discord.File(open("fuck.mp4", "rb")))

@bot.command()
async def help(ctx):
	embed=discord.Embed(title="Commands ", description="{ } means input required", color=embed_colour)
	embed.add_field(name="sudo shake {@target}", value="sudo get {subject_name} ", inline=True)
	embed.add_field(name="moves target between two channels rapidly", value="im gonna change this dw about it", inline=True)
	embed.add_field(name="sudo year {1,2,68, etc}", value="sudo game {minecraft}", inline=True)
	embed.add_field(name="Assigns a year role. Increments in August", value="Assigns you a game role for @mentions", inline=True)
	embed.add_field(name="sudo FUCK", value="", inline=True)
	embed.add_field(name="FUCK", value="", inline=True)
	await ctx.message.channel.send(embed=embed)

# Library Commands	

subjects = {
		"ENPH": "270 - http://93.174.95.29/main/CE1E90DC739863A9788F6324038E2DFB\nThe Bible - http://93.174.95.29/main/05D120938A4D7EBB5A706CE17F66B547",
		"MECH": "260/360 - http://93.174.95.29/main/4B6F6F6DF336EF7DB2219A8E66B1C498\n",
		"ELEC": "nothing here yet, but MNA >> Mesh",
		"PHYS": "250 - http://93.174.95.29/main/318C1507190566EA13AEB003893A7569\n",
		"MATH": "217 - http://www.math.ubc.ca/~CLP/CLP3/ & http://www.math.ubc.ca/~CLP/CLP4/\n255/257 - https://www.jirka.org/diffyqs/diffyqs.pdf\n",
		"CPEN": "https://stackoverflow.com/",
		"APSC": "https://mech2.sites.olt.ubc.ca/files/2014/12/S01_6161.jpg",
		"SPECS": "https://docs.google.com/spreadsheets/d/119mEbyerER02r8lSYzcT4sovFmxW48su0XgUqfFStf0/edit?usp=sharing",
		}

@bot.command()
async def get(ctx): 
	request = ctx.message.content.upper()

	if "SPECS" in request:
			embed = discord.Embed(title="Robot Summer component datasheets (WIP):", description=subjects["SPECS"], colour=embed_colour)
			await ctx.message.channel.send(embed=embed)

	elif "ALL" in request:
		for subject in subjects:
			await ctx.message.channel.send("**{} Textbooks:**".format(subject))
			await ctx.message.channel.send(subjects[subject])

	else:		
		for subject in subjects:
			if subject in request:	
				embed = discord.Embed(title="{} Textbooks:".format(subject), description=subjects[subject], colour=embed_colour)
				await ctx.message.channel.send(embed=embed)


# Role Management 

@bot.event
async def on_member_join(member):
	general = bot.get_channel(689295380474888245)
	embed = discord.Embed(
		description = '**Welcome to the Fizz Discord <@{}>!**\n\nAssign yourself a role by typing: ```sudo year <Your Year #>```'.format(member.id),
		colour = embed_colour
	)

	await general.send(embed=embed)
	await member.send(embed=embed)

# @bot.command()
# async def test(ctx):
# 	general = bot.get_channel(689295380474888245)
# 	embed = discord.Embed(
# 		description = '**Welcome to the Fizz Discord <@{}>!**\n\nAssign yourself a role by typing: ```sudo year <Your Year #>```'.format(ctx.author.id),
# 		colour = embed_colour
# 	)

# 	await general.send(embed=embed)
# 	await ctx.author.send(embed=embed)

years = {
	1: "Pre-EngPhys",
	2: "2nd Year",
	3: "3rd Year",
	4: "4th Year",
	5: "5th Year +",
}

rollover = {
	"Pre-EngPhys": "2nd Year",
	"2nd Year": "3rd Year",
	"3rd Year": "4th Year",
	"4th Year": "5th Year +",
	"5th Year +": "5th Year +"
}

# More as society changes
games = {
	"LEAGUE": "League of Legends",
	"CS": "CS:GO",
	"MINECRAFT": "Minecraft",
	"SMASH": "Smash"
}

@bot.command()
async def year(ctx):

	year = int(float(ctx.message.content[9:]))

	if year >= 5:
		year = 5

	role = discord.utils.get(ctx.guild.roles, name=years[year])
	role = discord.utils.get(ctx.guild.roles, name=years[year])

	# Adding / removing year role
	if role in ctx.message.author.roles:
		await ctx.message.author.remove_roles(role)
		embed = discord.Embed(description='**You are no longer {}**'.format(years[year]), colour=embed_colour)
		await ctx.message.channel.send(embed=embed)
	else:
		await ctx.message.author.add_roles(role)
		embed = discord.Embed(description='**You are now {}**'.format(years[year]), colour=embed_colour)
		await ctx.message.channel.send(embed=embed)

	# Clear any other year roles (Probably could be handled differently but it is almost 2am rn)
	for role in ctx.message.author.roles:
		if role.name in list(rollover.keys()) and role.name != years[year]:
			await ctx.message.author.remove_roles(role)




# TODO: make this command into a timed thing, maybe use the on_message to check if its sept 1st or not
@bot.command()
async def testroll(ctx):

	all_years = list(rollover.keys())
	
	for role in ctx.message.author.roles:
		if role.name in all_years:
			print(role)
			new_role = discord.utils.get(ctx.guild.roles, name=rollover[role.name])
			old_role = discord.utils.get(ctx.guild.roles, name=role.name)

			await ctx.message.author.remove_roles(old_role)
			await ctx.message.author.add_roles(new_role)
			break
		
@bot.command()
async def game(ctx):

	request = str(ctx.message.content[10:]).upper()

	role = discord.utils.get(ctx.guild.roles, name=games[request])
	if role in ctx.message.author.roles:
		await ctx.message.author.remove_roles(role)
		embed = discord.Embed(description = '**You no longer have the {} role**'.format(games[request]), colour = embed_colour)
		await ctx.message.channel.send(embed=embed)
	else:
		await ctx.message.author.add_roles(role)
		embed = discord.Embed(description = '**You were given the {} role**'.format(games[request]), colour = embed_colour)
		await ctx.message.channel.send(embed=embed)


# Just for Fun

# @bot.command()
# async def FUCK(ctx):

# 	await ctx.message.channel.send("https://cdn.discordapp.com/attachments/652016685750026240/713848400436527175/Terraria3.mp4")

bot.run("NzA3NDk0Mzk5NjA4NzUwMTIx.Xs627A.AAmCO5sAHfJwnas_ThvTC_2l2Bk")


# Regular methods
