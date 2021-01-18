import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import random
import asyncio
import json
import os
import wikipedia
import aiohttp


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun Cog Loaded Succesfully')

    @commands.command(
        cooldown_after_parsing=True,
        aliases=['8ball'],
        description="Chances of happening of given question")
    async def _8ball(self, ctx, *, question):
        responses = [
            'It is certain', 'It is decidedly so', 'Without a doubt',
            'Yes, definitely', 'You may rely on it', 'As i see it, yes',
            'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
            'Reply haze, try again', 'Ask again later',
            'Better not tell you now', 'Cannot predict now',
            'Concentrate and ask again', 'Do not count on it',
            'My reply is no', 'My sources say no', 'Outlook not so good',
            'Very doubtful'
        ]

        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="8ball",color=0xff0000)
        embed.add_field(name=f"Question: {question}",value=f"Reply: {random.choice(responses)}")
        await ctx.send(embed=embed)

    @commands.command(description="Kill a person :)")
    async def sendnuke(self, ctx, member: discord.Member):
        embed = discord.Embed(title="Nuke ", color=0xff0000)
        embed.add_field(
            name=f'{ctx.author} killed {member.name}',
            value='Misson Accomplished')
        embed.set_image(
            url=
            "https://media.tenor.com/images/e138ef6dcfc0f227e9ba27faf027c6ee/tenor.gif"
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def fml(self, ctx):
        url = "https://api.alexflipnote.dev/fml"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    url,
                    headers={
                        "Authorization":
                        f"FDGsCH8Kg3uEDyVBg-hJU16nH8s9Cl9Yr2hWG6Be"
                    }) as res:
                response = await res.json()
                resp = response['text']
                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title='FML',
                    description=f'{resp}',
                    color = 0xff0000
                )
                embed.set_footer(
                    text=f'Requested By: {ctx.author.name}',
                    icon_url=f'{ctx.author.avatar_url}')
                await ctx.send(embed=embed)

    @commands.command()
    async def say(self,ctx,tit,desc):
        if len(tit) > 60 or len(desc) > 80:
            await ctx.send('**Too big sentence**')
        else:
            embed = discord.Embed(
                title=tit,
                description=desc,
                color=0x1abc9c
            )
            await ctx.send(embed=embed)
        


    
def setup(client):
    client.add_cog(Fun(client))

