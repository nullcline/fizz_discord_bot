import discord
from discord.ext import commands

embed_colour = discord.Colour.red()
# Message ID for the role assignment message
role_message = 754224412286517279
# Channel ID for the role assignment channel
role_channel = 752430500462854215
# Probably not the best way to do this but alas i am a monkey
emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','♾️']
emoji_to_role = {
    '1️⃣':0,
    '2️⃣':1,
    '3️⃣':2, 
    '4️⃣':3,
    '5️⃣':4,
    '♾️':5
}

# Rollover organization for roles
rollover = {
        "Pre-EngPhys": "2nd Year",
        "2nd Year": "3rd Year",
        "3rd Year": "4th Year",
        "4th Year": "5th Year +",
        "5th Year +": "5th Year +",
    }

class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Need to do this extra retrieving steps because on_reaction_add/remove doesn't work with old memories
        # (not in cache) so the raw version that gives the payload only must be used
        self.fizz = bot.get_guild(689295380474888194)
        self.year_roles = [
            discord.utils.get(self.fizz.roles, name="Pre-EngPhys"),
            discord.utils.get(self.fizz.roles, name="2nd Year"),
            discord.utils.get(self.fizz.roles, name="3rd Year"),
            discord.utils.get(self.fizz.roles, name="4th Year"),
            discord.utils.get(self.fizz.roles, name="5th Year +"),
            discord.utils.get(self.fizz.roles, name="Alumnus")
        ]

        print("roles.py: Done retrieving guild and roles")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Checks the input reaction against all of the ones previously listed, if the member has the corresponding 
        # role and it isn't the input reaction, remove that role and reaction. After, give them the input reaction role.

        # Probably need to add try/catch but it seems to work fine without it
        emoji = payload.emoji.name
        post = await self.bot.get_channel(role_channel).fetch_message(role_message)
        member = self.fizz.get_member(payload.user_id)

        if (payload.message_id == role_message) :
            
            # Remove all previous reactions and roles
            for e in emojis:
                if e != emoji and self.year_roles[emoji_to_role[e]] in member.roles:
                    await member.remove_roles(self.year_roles[emoji_to_role[e]])
                    await post.remove_reaction(e, member)

            # Add new role
            await member.add_roles(self.year_roles[emoji_to_role[emoji]])

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Simply removes the role that corresponds to the reaction that was removed from the message
        emoji = payload.emoji.name
        member = self.fizz.get_member(payload.user_id)

        if (payload.message_id == role_message) :

            # Remove role
            await member.remove_roles(self.year_roles[emoji_to_role[emoji]])

    # Updates year standing. Only Andrew can use this :) hi
    @commands.command()
    @commands.is_owner()
    async def supersecretcommandname(self, ctx):

        all_years = list(rollover.keys())
        members = ctx.guild.members

        for member in members:
            print(member.roles)
            for role in member.roles:
                if role.name in all_years:
                    new_role = discord.utils.get(
                        ctx.guild.roles, name=rollover[role.name]
                        )
                    old_role = discord.utils.get(ctx.guild.roles, name=role.name)
                    print(new_role)
                    print(old_role)

                    await member.remove_roles(old_role)
                    await member.add_roles(new_role)
                    break
    
def setup(bot):
    bot.add_cog(RolesCog(bot))