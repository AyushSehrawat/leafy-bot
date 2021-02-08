import os

import discord
import motor.motor_asyncio
import nest_asyncio
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from pymongo import MongoClient

nest_asyncio.apply()
mongo_url = os.environ.get("MONGO_URL")

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

predb = cluster["discord"]["prefix"]


class NewInfo(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_ready(self):
        print("New Info Cog Loaded Succesfully")

    @commands.command(aliases=["si", "serverinfo"])
    async def server(self, ctx):
        stats = await predb.find_one({"guild": ctx.guild.id})
        if stats is None:
            pre = "--"
        else:
            pre = stats["prefix"]
        own = ctx.guild.owner
        reg = str(ctx.guild.region)
        ver = str(ctx.guild.verification_level)
        tim = str(ctx.guild.created_at)
        txt = len(ctx.guild.text_channels)
        vc = len(ctx.guild.voice_channels)
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="<:info2:799169805747224606> Server Info",
            color=0xFF0000,
        )
        embed.add_field(name=":ballot_box: Name", value=f"{ctx.guild}")
        embed.add_field(name=":crown: Owner", value=f"{own.mention}")
        embed.add_field(
            name="<a:devstar:799173767707885588> Members",
            value=f"{ctx.guild.member_count}",
        )
        embed.add_field(
            name="<a:earth:799175818285809706> Region", value=f"{reg.capitalize()}"
        )
        embed.add_field(
            name="<a:devcheck:799178026729734166> Verification",
            value=f"Level -{ver.capitalize()}",
        )
        embed.add_field(name=":calendar: Created At", value=f"{tim[0:11]}")
        embed.add_field(
            name="<:channels:799230731397890049> Text Channels", value=f"{txt}"
        )
        embed.add_field(
            name="<:channels:799230731397890049> Voice Channels", value=f"{vc}"
        )
        embed.add_field(
            name="<a:prefix:799189793589821461> Prefix", value=f"`{pre}`", inline=False
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["bi", "about"])
    async def bot(self, ctx):
        ser = len(self.client.guilds)
        mem = len(self.client.users)
        stats = await predb.find_one({"guild": ctx.guild.id})
        if stats is None:
            pre = "--"
        else:
            pre = stats["prefix"]
        embed = discord.Embed(
            timestamp=ctx.message.created_at, title=":robot:  Bot Info", color=0xFF0000
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(
            name="<:dotty:799513382113640468> Helping", value=f"{ser} servers"
        )
        embed.add_field(
            name="<a:devhello:799514685610917908> Serving", value=f"{mem} members"
        )
        embed.add_field(name="<a:prefix:799189793589821461> Prefix", value=f"`{pre}`")
        embed.add_field(
            name="<a:devserver:799517828629659689> Support Server",
            value="[Join My Server](https://dsc.gg/leafyserver)",
        )
        embed.add_field(
            name="<a:devdia:799519773536288838> Add Me",
            value="[Click Here to Add Me](https://dsc.gg/leafy)",
        )
        embed.add_field(
            name="<a:earth:799175818285809706> Website",
            value="[Checkout my website](https://leafy.algoriq.live)",
        )
        embed.add_field(
            name="<:minilight:799521289026142249> Made By", value="Mini.py#5183"
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["ui", "userinfo"])
    async def user(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        else:
            pass
        c = str(member.created_at)[0:11]
        j = str(member.joined_at)[0:11]
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="<a:devstar:799173767707885588> User Info",
            color=0xFF0000,
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=":name_badge: Name", value=f"{member.name}")
        embed.add_field(
            name="<a:happyblob:793040737267744768> Nickname", value=f"{member.nick}"
        )
        embed.add_field(name=":credit_card: Id", value=f"{member.id}")
        embed.add_field(name=":flower_playing_cards: Joined Discord", value=f"{c}")
        embed.add_field(
            name="<a:devcheck:799178026729734166> Joined Server", value=f"{j}"
        )
        embed.add_field(
            name="<:info2:799169805747224606> Highest Role",
            value=f"{member.top_role.mention}",
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(NewInfo(client))
