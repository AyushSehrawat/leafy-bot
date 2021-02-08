import discord
from discord.ext import commands


class Slowmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slowmode cog loaded successfully")

    @commands.command(aliases=["slow"], description="Changes the slowmode of channel")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds <= 21600 and seconds > 0:
            embed = discord.Embed(Title=f"Slowmode ", color=0xFF0000)

            embed.add_field(
                name=f"Slowmode Changed !",
                value=f"Slowmode is now set to {seconds} seconds",
            )
            embed.set_image(
                url="https://media1.tenor.com/images/27b559e217424b733741a34f4a5c24c6/tenor.gif"
            )

            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )

            await ctx.channel.edit(slowmode_delay=seconds)

            await ctx.send(embed=embed)

        else:
            await ctx.send("Slowmode cannot be more than 21600 seconds or 0 and less")

    @commands.command(aliases=["rslow"], description="Changes slowmode back to 0")
    @commands.has_permissions(manage_channels=True)
    async def resetslow(self, ctx):

        embed = discord.Embed(Title=f"Slowmode ", color=0xFF0000)

        embed.add_field(name=f"Slowmode Changed !", value=f"Slowmode is now set to 0")

        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )

        await ctx.channel.edit(slowmode_delay=0)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Slowmode(client))
