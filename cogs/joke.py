from discord.ext import commands
import requests
import discord


class Joke(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Joke cog loaded successfully')

    @commands.command()
    async def joke(self, ctx):
        try:
            url = "https://joke3.p.rapidapi.com/v1/joke"

            headers = {
                'x-rapidapi-key':
                "fefb761607mshbf25f11ccc8b263p1d41bfjsn20dfefe445d1",
                'x-rapidapi-host':
                "joke3.p.rapidapi.com"
            }

            resp = requests.get(url, headers=headers)
            response = resp.json()
        

            joke = response['content']
            upv = response['upvotes']
            dov = response['downvotes']

            nsfw = response['nsfw']
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                title='<:lol:799661616127410196> Joke',
                color=0xff0000
            )
            if nsfw == 'true':
                embed.add_field(
                    name=f'|| {joke} ||',
                    value=f':thumbsup: - {upv} :thumbsdown: - {dov}'
                )
            else:
                embed.add_field(
                    name=f'{joke}',
                    value=f':thumbsup: - {upv} :thumbsdown: - {dov}'
                )

            await ctx.send(embed=embed)
        except:
            await ctx.send("**Something went wrong :( , report Mini.py#5183")

def setup(client):
    client.add_cog(Joke(client))
