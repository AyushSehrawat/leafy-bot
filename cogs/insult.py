from discord.ext import commands
import aiohttp
import discord
from discord.ext.commands import cooldown, BucketType


class Fancy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Insult cog loaded successfully')

    @commands.command(description="Roasts :)")
    async def roast(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'https://insult.mattbas.org/api/insult') as response:
                    insult = await response.text()
                    embed = discord.Embed(
                        timestamp=ctx.message.created_at,
                        title=f"{member.name}",
                        description=f"{insult}",
                        color=0xff0000)
                    await ctx.send(embed=embed)

        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'https://insult.mattbas.org/api/insult') as response:
                    insult = await response.text()
                    embed = discord.Embed(
                        timestamp=ctx.message.created_at,
                        title=f"{member.name}",
                        description=f"{insult}",
                        color=0xff0000)
                    await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fancy(client))
