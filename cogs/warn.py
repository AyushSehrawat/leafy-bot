import discord
from discord.ext import commands
from pymongo import MongoClient
import sys
import asyncio
import motor.motor_asyncio
import nest_asyncio
nest_asyncio.apply()

sys.path.append("/MiniBot/discord_pass.py")
import os

mongo_url = os.environ.get('MONGO_URL')

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
import discord_pass

warndb = cluster["discord"]["warn"]


class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Warn cog loaded successfully')

    @commands.command(
        aliases=['w'],
        description='Warn a user ( If limit > 5 , the member is banned )')
    @commands.has_permissions(ban_members=True)
    async def warn(self,ctx,member: discord.Member,warns=1,*,reason = 'Not specified'):
        guild = ctx.guild
        if guild.me.top_role < member.top_role:
            await ctx.send('**He is higher than me in hierarchy**')
        elif member.bot:
            await ctx.send('**You cannot warn bot**')
        elif member == ctx.author:
            await ctx.send('**You cannot warn yourself**')
        elif member != ctx.author:
            
            if len(reason) > 60:
                await ctx.send('**Very big reason**')
            else:

                stats = await warndb.find_one({"id": member.id})

                if member == self.client.user:
                    await ctx.send('**Haha, i am immortal**')
                elif stats is None and warns <= 5:
                    passwor = discord_pass.secure_password_gen(10)
                    passwor = str(passwor)
                    newuser =     {"id":member.id, "Cases" : [[passwor, reason,ctx.author.mention,warns]],'warns' : warns}
                    await warndb.insert_one(newuser)
                    embed = discord.Embed(
                        title="Warn",
                        description=
                        f"{member.name} has been warned with {warns} warn(s) for `{reason}` ",
                        color=0xff0000)
                    await ctx.send(embed=embed)

                elif warns > 5:
                    embed = discord.Embed(
                        title="Invalid usage",
                        description="You cannot give more than 5 warns",
                        color=0xff0000)
                    embed.set_image(
                        url=
                        "https://media1.tenor.com/images/7cb7b5cc74e9a63d11e474a3e135d617/tenor.gif"
                    )
                    await ctx.send(embed=embed)

                else:
                    passwor = discord_pass.secure_password_gen(10)
                    passwor = str(passwor)
                    total_warn = stats["warns"] + warns
                    await warndb.update_one({
                        "id": member.id
                    }, {"$set": {
                        "warns": total_warn
                    }})
                    await warndb.update({ 'id': member.id },{"$addToSet":{"Cases":[passwor, reason,ctx.author.mention,warns]}})
            
                    embed = discord.Embed(
                        title="Warn",
                        description=
                        f"{member.name} has been warned with {warns} warn(s) for `{reason}` ",
                        color=0xff0000)
                    await ctx.send(embed=embed)

                    if total_warn >= 5:
                        await member.ban(reason="Exceeded The Warn Limit")
                        embed = discord.Embed(
                            title="Warn",
                            description=
                            f"{member.name} has been banned since he exceeded the warn limit",
                            color=0xff0000)
                        await ctx.send(embed=embed)





    @commands.command(
        description='Shows your warns'
    )
    async def warns(self,ctx):
        stats = await warndb.find_one({"id": ctx.author.id})
        if stats is None:
            await ctx.send(f'**No data found for {ctx.author.name}**')
        else:
            total_warns = stats['warns'] 
            await ctx.author.send(f'**You have {total_warns} warns**')
            await ctx.send('**Please check your private messages for total warns**')

    @commands.command(
        description='Shows the case id, reason and total warns of mentioned user/id'
    )
    @commands.has_permissions(ban_members=True)
    async def case(self,ctx,member : discord.Member):
        stats = await warndb.find_one({"id": member.id})
        if stats is None:
            await ctx.send('**No Data Found**')
        else:
            total_warns = stats['warns']
            embed = discord.Embed(
                title=f'Case - {member.name}',
                color = 0xff0000
            )

            for x in stats['Cases']:
                embed.add_field(
                    name=f'Id - {x[0]}',
                    value=f"Reason - {x[1]}\nWarned By - {x[2]}\nWarn(s) given = {x[3]}" ,
                    inline=False
                )
            embed.add_field(
                name='Total warns',
                value=f'{total_warns}',
                inline=False
            )
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(
        aliases=['cw'],
        description='Clears the data of mentioned user / id'
    )
    @commands.has_permissions(ban_members=True)
    async def clearwarns(self,ctx,member : discord.Member):
        stats = await warndb.find_one({"id": member.id})
        if stats is None:
            await ctx.send('No Data Found')
        else:
            await warndb.delete_one({'id' : member.id})
            await ctx.send('**Record Cleared**')




def setup(client):
    client.add_cog(Warn(client))