import discord
from discord.ext import commands

embed_colour = discord.Colour.red()

# TODO Replace this with a reaction based system with custom emotes
# Dictionary of games
games = {
    "LEAGUE": "League of Legends",
    "CS": "CS:GO",
    "MINECRAFT": "Minecraft",
    "SMASH": "Smash",
    "VALORANT": "Valorant",
    "AU": "Among Us",
}


class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        print("games.py: Ready")

    @commands.command()
    @commands.guild_only()
    async def game(self, ctx):
        # Finds requested game from dictionary then toggles the role onto the user

        request = str(ctx.message.content[10:]).upper()

        role = discord.utils.get(ctx.guild.roles, name=games[request])
        if role in ctx.message.author.roles:
            await ctx.message.author.remove_roles(role)
            embed = discord.Embed(
                description="**You no longer have the {} role**".format(games[request]),
                colour=embed_colour,
            )
            await ctx.message.channel.send(embed=embed)
        else:
            await ctx.message.author.add_roles(role)
            embed = discord.Embed(
                description="**You were given the {} role**".format(games[request]),
                colour=embed_colour,
            )
            await ctx.message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(GamesCog(bot))
