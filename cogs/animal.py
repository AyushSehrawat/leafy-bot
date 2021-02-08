import os

import aiohttp
import discord
from discord.ext import commands

alex = os.environ.get("ALEX")


class Animal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Animal cog loaded successfully")

    @commands.command(aliases=["meow"])
    async def cat(self, ctx):
        url = "https://api.alexflipnote.dev/cats"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, headers={"Authorization": f"{alex}"}) as res:
                response = await res.json()
                pic = response["file"]
                embed = discord.Embed(
                    timestamp=ctx.message.created_at, title="Cat", color=0xFF0000
                )
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                embed.set_image(url=pic)
                await ctx.send(embed=embed)

    @commands.command(aliases=["doggo"])
    async def dog(self, ctx):
        url = "https://api.alexflipnote.dev/dogs"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, headers={"Authorization": f"{alex}"}) as res:
                response = await res.json()
                pic = response["file"]
                embed = discord.Embed(
                    timestamp=ctx.message.created_at, title="Dog", color=0xFF0000
                )
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                embed.set_image(url=pic)
                await ctx.send(embed=embed)

    @commands.command()
    async def bird(self, ctx):
        url = "https://api.alexflipnote.dev/birb"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, headers={"Authorization": f"{alex}"}) as res:
                response = await res.json()
                pic = response["file"]
                embed = discord.Embed(
                    timestamp=ctx.message.created_at, title="Bird", color=0xFF0000
                )
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                embed.set_image(url=pic)
                await ctx.send(embed=embed)

    @commands.command()
    async def sadcat(self, ctx):
        url = "https://api.alexflipnote.dev/sadcat"
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, headers={"Authorization": f"{alex}"}) as res:
                response = await res.json()
                pic = response["file"]
                embed = discord.Embed(
                    timestamp=ctx.message.created_at, title="Sad Cat", color=0xFF0000
                )
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                embed.set_image(url=pic)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Animal(client))
