import discord
from asyncio import sleep
from discord.ext import commands

embed_colour = discord.Colour.red()
shake_room1 = 709974781252075640
shake_room2 = 709974744329486346
access_role = 689296629836415022
joy_list = ["JOY", "BLESSED", "COMFORT", "HAPPY", "RELIEF", "WELLNESS", "POG"]

class UtilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def say(self, ctx):
        if (ctx.message.author.id == 168388106049814528):
            embed = discord.Embed(
            description=ctx.message.content[8:],
            colour=embed_colour,
            )
            await ctx.message.channel.send(embed=embed)

    # Customizable Command for me to do whatever the hell I want
    @commands.command()
    @commands.is_owner()
    async def ac(self, ctx):
        if (ctx.message.author.id == 168388106049814528):
            pass

        
    @commands.command(aliases=["shake", "airstrike", "nuke", "discombobulate", "summon"])
    @commands.guild_only()
    async def s(self, ctx):
        # Spam pings the target :)

        target = ctx.message.mentions[0]

        if (ctx.message.mention_everyone):
            pass

        else:
            for _ in range(4):
                await target.send("Get in Discord <@{}> >:(".format(target.id))
                await sleep(0.2)

    @commands.command()
    @commands.guild_only()
    async def gag(self, ctx):
        if True:
            print("heh")


    @commands.command()
    @commands.guild_only()
    async def ungag(self, ctx):
        if True:
            print("heh")


    # @commands.command()
    # @commands.guild_only()
    # async def echo(self, ctx):

    #     msg = ctx.message.content[9:]

    #     if ctx.author.id == 722364047839723561 or msg.upper() == "FUCK" or msg.upper() == "PAIN" or msg.upper() in joy_list:
    #         pass

    #     else:

    #         for _ in range(5):
    #             await ctx.message.channel.send(msg)
    #             await sleep(0.5)


    @commands.command(aliases=["j", "joi"])
    @commands.guild_only()
    async def join(self, ctx):
        global voice
        channel = ctx.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f"Joined {channel}")
    
def setup(bot):
    bot.add_cog(UtilCog(bot))