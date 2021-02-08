import discord
import requests
from discord.ext import commands


class LC(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("LC cog loaded successfully")

    @commands.command(aliases=["lovecalculator"])
    async def lc(self, ctx, name1, name2):
        try:
            if len(name1) > 30 or len(name2) > 30:
                await ctx.send("**Big Names**")
            else:
                url = "https://love-calculator.p.rapidapi.com/getPercentage"

                querystring = {"fname": f"{name1}", "sname": f"{name2}"}

                headers = {
                    "x-rapidapi-key": "fefb761607mshbf25f11ccc8b263p1d41bfjsn20dfefe445d1",
                    "x-rapidapi-host": "love-calculator.p.rapidapi.com",
                }

                respo = requests.request(
                    "GET", url, headers=headers, params=querystring
                )
                response = respo.json()
                per = response["percentage"]
                result = response["result"]
                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title=":heart: Love Calculator",
                    color=0xFF0000,
                )
                embed.add_field(
                    name=f"\n{name1} :hearts: {name2}", value=f"{per}% - {result}"
                )
                await ctx.send(embed=embed)

        except Exception:
            raise Exception


def setup(client):
    client.add_cog(LC(client))
