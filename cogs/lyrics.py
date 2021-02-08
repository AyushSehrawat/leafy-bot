import discord
import requests
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown


class Lyrics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Lyrics cog loaded successfully")

    @commands.command(aliases=["lyrics"], description="Shows the lyrics of given song")
    @cooldown(1, 30, BucketType.user)
    async def ly(self, ctx, *, lyrics):
        if lyrics is None:
            await ctx.send("You forgot lyrcis")
        else:
            words = "+".join(lyrics.split(" "))
            print(words)
            URL = f"https://some-random-api.ml/lyrics?title={words}"

            def check_valid_status_code(request):
                if request.status_code == 200:
                    return request.json()

                return False

            def get_song():
                request = requests.get(URL)
                data = check_valid_status_code(request)

                return data

            song = get_song()
            if not song:
                await ctx.channel.send("Couldn't get lyrcis from API. Try again later.")

            else:
                music = song["lyrics"]
                ti = song["title"]
                au = song["author"]

                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    Title="Title: Song",
                    color=0xFF0000,
                )

                embed.add_field(name=f"Title: {ti}", value=f"Author: {au}")

                chunks = [music[i : i + 1024] for i in range(0, len(music), 2000)]
                for chunk in chunks:
                    embed.add_field(name="\u200b", value=chunk, inline=False)

                # embed.add_field(name='Song',value=f'{music}', inline=True)
                embed.set_footer(
                    text=f"Requested By: {ctx.author.name}",
                    icon_url=f"{ctx.author.avatar_url}",
                )
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Lyrics(client))
