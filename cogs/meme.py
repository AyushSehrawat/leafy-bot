import discord
import requests
from discord.ext import commands


class Meme(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Meme cog loaded successfully")

    @commands.command(description="Shows a random meme")
    async def meme(self, ctx):
        #
        URL = f"https://meme-api.herokuapp.com/gimme"

        def check_valid_status_code(request):
            if request.status_code == 200:
                return request.json()

            return False

        def get_meme():
            request = requests.get(URL)
            data = check_valid_status_code(request)

            return data

        memee = get_meme()
        if not memee:
            await ctx.channel.send("Couldn't get meme from API. Try again later.")

        else:
            caption = memee["title"]
            img = memee["url"]
            nsfw = memee["nsfw"]
            spoiler = memee["spoiler"]
            if nsfw == "true" or spoiler == "true":
                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title=f"||{caption}||",
                    color=0xFF0000,
                )
                embed.set_image(url=f"SPOILER_{img}")
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    timestamp=ctx.message.created_at, title=f"{caption}", color=0xFF0000
                )
                embed.set_image(url=f"{img}")
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Meme(client))
