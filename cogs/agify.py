from discord.ext import commands
import requests
import discord
import datetime


class Agify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Agify cog loaded successfully')

    @commands.command(
        description="Guess age of given name")
    async def ga(self, ctx, name):
        if name == None:
            await ctx.send('You forgot name')
        else:
            name = str(name)
            URL = f'https://api.agify.io/?name={name}'

            def check_valid_status_code(request):
                if request.status_code == 200:
                    return request.json()

                return False

            def get_age():
                request = requests.get(URL)
                data = check_valid_status_code(request)

                return data

            age = get_age()
            if not age:
                await ctx.channel.send(
                    "Couldn't get age from API. Try again later.")

            else:
                agee = str(age['age'])
                embed = discord.Embed(
                    title='Age Guess',
                    description='Guesses the age of given name!',
                    color=0xff0000)
                embed.add_field(
                    name=name, value=f'I guess he is {agee} years old')
                embed.set_footer(
                    text=f'Requested By: {ctx.author.name}',
                    icon_url=f'{ctx.author.avatar_url}')
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Agify(client))
