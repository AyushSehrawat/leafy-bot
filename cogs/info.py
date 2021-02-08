import datetime
import os

import discord
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info Cog Loaded Succesfully")

    @commands.command(hidden=True)
    async def spoon(self, ctx):
        embed = discord.Embed(title="Spoonfeeding", description=None, color=0xFF0000)
        embed.add_field(
            name="Not here",
            value="Spoon feeding is considered bad practice here as it can make the learner dependent on others, and programming isn't just writing code but also figuring out the logic and stuff for a given process. Something you don't do when you are spoon fed. In short terms, people learn from trial and error.",
        )

        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )

        await ctx.send(embed=embed)

    @commands.command(description="Check Bot Latency")
    async def ping(self, ctx):
        embed = discord.Embed(color=0xFF0000)
        embed.add_field(
            name="\u200b",
            value=f"<a:loading:800583154951651348> Bot latency - {round(self.client.latency * 1000)}ms",
            inline=False,
        )
        embed.set_author(
            name="Latency",
            icon_url="https://store-images.s-microsoft.com/image/apps.24298.14073362953807348.18acabda-19d7-4bf5-8056-352b7495ecef.fc31be50-f27e-4c81-9b14-18c06c40e837?mode=scale&q=90&h=270&w=270&background=%23FFFFFF",
        )

        await ctx.send(embed=embed)

    @commands.command(description="Sends your avatar pic or of mentioned user / id")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
            a = member.avatar_url
            await ctx.send(a)
        else:
            a = member.avatar_url

            await ctx.send(a)

    @commands.command(aliases=["mem"], description="Shows total member in the server")
    @cooldown(1, 5, BucketType.user)
    async def memcount(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild}",
            description=f"There are {ctx.guild.member_count} members in this server",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)

    @commands.command(description="Invite bot to your server")
    @cooldown(1, 1800, BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Hi! Use these links to add me or join my support server",
            description="**[Add Me](https://discord.com/api/oauth2/authorize?client_id=791888515100573727&permissions=1610477559&scope=bot) | [Support Server](https://discord.gg/grr47CR8y8)**",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def totalcmds(self, ctx):
        await ctx.send(f"There are {len(self.client.commands)} commands")

    @commands.command(hidden=True)
    async def emoji(self, ctx):
        if ctx.author.id == 727365670395838626:
            for emoji in ctx.guild.emojis:
                print(f"{emoji.id} - {emoji.name}")
            await ctx.message.delete()

    @commands.command(description="Vote Leafy")
    async def vote(self, ctx):
        embed = discord.Embed(
            title="Vote leafy !",
            description="**[Vote Here](https://voidbots.net/bot/791888515100573727/)**",
            color=0xFF0000,
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))
